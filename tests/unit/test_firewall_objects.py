"""Offline conformance to the supplied FMG 7.6.7 / FortiOS 7.4 firewall schema."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from pyfortinet.exceptions import FMGWrongRequestException
from pyfortinet.fmg_api.firewall import Address, InternetService, ProxyAddress, ProxyAddressGroup

from .conftest import resolve

CASES = [
    (ProxyAddress, "proxy_address", "proxy-address"),
    (ProxyAddressGroup, "proxy_address_group", "proxy-addrgrp"),
    (InternetService, "internet_service", "internet-service"),
]


def reference(filename):
    return json.loads((Path(__file__).parent / "fixtures" / ("firewall_" + filename + ".json")).read_text())


def sample(schema, definitions):
    if "$ref" in schema:
        return sample(definitions[schema["$ref"].split("/")[-1]], definitions)
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema["type"]
    if kind == "object":
        return {key: sample(value, definitions) for key, value in schema["properties"].items()}
    if kind == "array":
        return [sample(schema["items"], definitions)]
    if kind == "integer":
        return 1
    return "12345678-1234-1234-1234-123456789abc" if schema.get("format") == "uuid" else "example"


def schema_fields():
    for model, filename, api_name in CASES:
        spec = reference(filename)
        for name, definition in spec["definitions"]["pm.config.firewall." + api_name]["properties"].items():
            yield pytest.param(model, name, definition, spec["definitions"], id=model.__name__ + ":" + name)


@pytest.mark.parametrize("model, name, definition, definitions", list(schema_fields()))
def test_schema_fields_round_trip(model, name, definition, definitions):
    values = definition.get("enum", [sample(definition, definitions)])
    if "enum" in definition.get("items", {}):
        values = [definition["items"]["enum"]]
    for value in values:
        obj = model.model_validate({name: value})
        assert obj.model_dump(by_alias=True, exclude_none=True) == {name: value}
        python_name = name.lstrip("_").replace("-", "_")
        assert model(**{python_name: value}).model_dump(by_alias=True, exclude_none=True) == {name: value}
    assert model(**{name: None}).model_dump(by_alias=True, exclude_none=True) == {}


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("scope", ["root", "global", "other"])
def test_get_preserves_fields_and_scope(client, post, case, scope):
    model, filename, api_name = case
    spec = reference(filename)
    data = sample(spec["definitions"]["pm.config.firewall." + api_name], spec["definitions"])
    post.return_value = {"status": {"code": 0}, "data": [data]}
    obj = resolve(client.get(model, scope=scope)).first()
    assert obj.model_dump(by_alias=True, exclude_none=True) == data
    expected_scope = "global" if scope == "global" else "adom/" + scope
    assert obj.fmg_scope == expected_scope
    assert obj._fmg is client
    assert post.call_args.kwargs["request"]["params"][0]["url"] == (
        "/pm/config/" + expected_scope + "/obj/firewall/" + api_name
    )


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("method", ["add", "set", "update", "delete", "clone"])
@pytest.mark.parametrize("scope", ["root", "global"])
def test_write_routes(client, post, case, method, scope):
    model, filename, api_name = case
    post.return_value = {"status": {"code": 0}}
    identity = {"id": 1} if model is InternetService else {"name": "example"}
    obj = model(**identity, fmg_scope=scope)
    kwargs = ({"id": 2} if model is InternetService else {"name": "copy"}) if method == "clone" else {}
    if model is InternetService and method not in ("set", "update"):
        with pytest.raises(FMGWrongRequestException, match="GET, SET, and UPDATE"):
            resolve(getattr(client, method)(obj, **kwargs))
        post.assert_not_called()
        return
    assert resolve(getattr(client, method)(obj, **kwargs)).success
    expected_scope = "global" if scope == "global" else "adom/" + scope
    url = "/pm/config/" + expected_scope + "/obj/firewall/" + api_name
    if method != "add" and model is not InternetService:
        url += "/example"
    sent = post.call_args.kwargs["request"]["params"][0]
    assert sent["url"] == url
    assert post.call_args.kwargs["request"]["method"] == method
    if method in ("add", "set", "update"):
        assert sent["data"] == identity
    elif method == "clone":
        assert sent["data"] == {"name": "copy"}


def test_proxy_address_references_and_switches():
    obj = ProxyAddress(host=[Address(name="first"), "second"], case_sensitivity=1, method="get")
    assert obj.model_dump(by_alias=True, exclude_none=True) == {
        "host": ["first", "second"],
        "case-sensitivity": "enable",
        "method": ["get"],
    }
    with pytest.raises(ValidationError):
        ProxyAddress(host=Address())
    with pytest.raises(ValidationError):
        ProxyAddress(type="invalid")


def test_proxy_group_members_are_name_arrays():
    group = ProxyAddressGroup(member=[ProxyAddress(name="first"), "second"], type="dst")
    assert group.model_dump(exclude_none=True) == {"member": ["first", "second"], "type": "dst"}
    assert ProxyAddressGroup(member=[]).model_dump(exclude_none=True) == {"member": []}
    assert ProxyAddressGroup(member=None).model_dump(exclude_none=True) == {}
    assert "dynamic_mapping" not in ProxyAddressGroup.model_fields
    assert "dynamic_mapping" not in ProxyAddress.model_fields


def test_internet_service_lookup_uses_id_filter(client, post):
    service_id = 65536
    post.return_value = {"status": {"code": 0}, "data": [{"id": service_id, "name": "example"}]}
    service = resolve(client.get(InternetService(id=service_id))).first()
    sent = post.call_args.kwargs["request"]["params"][0]
    assert sent["url"] == "/pm/config/adom/root/obj/firewall/internet-service"
    assert sent["filter"] == ["id", "==", service_id]
    assert service.id == service_id
    assert "dynamic_mapping" not in InternetService.model_fields
