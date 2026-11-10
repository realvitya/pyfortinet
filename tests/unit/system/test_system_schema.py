"""Device models accept the supplied FMG 7.6.7 / FortiOS 7.4 schema shapes."""

import json
from ipaddress import IPv4Interface
from pathlib import Path

import pytest
from pydantic import ValidationError

from pyfortinet.fmg_api.dvmdb import VDOM
from pyfortinet.fmg_api.system import DeviceInterface, DeviceZone, SystemAdmin
from tests.unit.conftest import resolve

REFERENCE = json.loads((Path(__file__).parents[1] / "fixtures" / "system_device_schema.json").read_text())
DEFINITIONS = REFERENCE["definitions"]
INTERFACE = DEFINITIONS["pm.config.system.interface"]["properties"]


def example(schema):
    """Build a populated wire example from the independent reference, including subtables."""
    if "$ref" in schema:
        return example(DEFINITIONS[schema["$ref"].split("/")[-1]])
    if "enum" in schema:
        return schema["enum"][0]
    if schema["type"] == "object":
        return {name: example(value) for name, value in schema["properties"].items()}
    if schema["type"] == "array":
        return (
            ["192.0.2.1", "255.255.255.0"]
            if schema["items"].get("format") == "IPv4 address/mask"
            else [example(schema["items"])]
        )
    if schema["type"] == "integer":
        return 1
    return string_example(schema)


def string_example(schema):
    """Return documentation-shaped addresses without imposing additional constraints."""
    if "IPv6" in schema.get("format", ""):
        return "2001:db8::1/64" if "prefix" in schema["format"] else "2001:db8::1"
    if "IPv4" in schema.get("format", ""):
        return "192.0.2.1"
    return "example"


@pytest.mark.parametrize("api_name", INTERFACE)
def test_every_interface_schema_field_is_retained(api_name):
    schema = INTERFACE[api_name]
    values = schema.get("enum", [example(schema)])
    if "enum" in schema.get("items", {}):
        values = [schema["items"]["enum"]]
    for value in values:
        obj = DeviceInterface.model_validate({api_name: value})
        payload = obj.model_dump(by_alias=True, exclude_none=True)
        expected = value
        if api_name in ("ip", "management-ip"):
            expected = IPv4Interface("/".join(value)).compressed
        assert payload == {api_name: expected}
        python_name = api_name.replace("-", "_")
        assert DeviceInterface(**{python_name: value}).model_dump(by_alias=True, exclude_none=True) == payload


@pytest.mark.parametrize("api_name", INTERFACE)
def test_interface_fields_can_be_absent_or_null(api_name):
    assert DeviceInterface(**{api_name: None}).model_dump(by_alias=True, exclude_none=True) == {}


def test_interface_partial_reply_and_invalid_media():
    assert DeviceInterface.model_validate({"name": "port1"}).mediatype is None
    with pytest.raises(ValidationError):
        DeviceInterface(mediatype="invalid-media")


def test_get_preserves_new_interface_fields(client, post):
    payload = {
        "name": "port1",
        "mediatype": "sr",
        "snmp-index": 7,
        "secondaryip": [{"id": 1, "ip": ["192.0.2.1", "255.255.255.0"], "allowaccess": ["ping"]}],
        "ipv6": {"ip6-address": "2001:db8::1/64"},
    }
    post.return_value = {"status": {"code": 0}, "data": [payload]}
    response = resolve(client.get(DeviceInterface(device="FG01")))
    obj = response.first()
    assert obj.model_dump(by_alias=True, exclude_none=True) == payload


def test_add_serializes_new_fields_and_nested_rows(client, post):
    post.return_value = {"status": {"code": 0}, "data": [{"name": "example"}]}
    obj = DeviceInterface(
        device="FG01",
        name="example",
        mediatype="sr",
        vlan_protocol="8021ad",
        client_options=[{"id": 1, "code": 12, "type": "string", "value": "example"}],
        vrrp=[{"vrid": 1, "vrip": "192.0.2.1"}],
    )
    assert resolve(client.add(obj)).success
    request = post.call_args.kwargs["request"]["params"][0]
    assert request["url"] == "/pm/config/device/FG01/global/system/interface"
    assert request["data"] == {
        "name": "example",
        "mediatype": "sr",
        "vlan-protocol": "8021ad",
        "client-options": [{"id": 1, "code": 12, "type": "string", "value": "example"}],
        "vrrp": [{"vrid": 1, "vrip": "192.0.2.1"}],
    }


@pytest.mark.parametrize("model, key", [(SystemAdmin, "admin"), (DeviceZone, "zone")])
def test_other_system_models_match_schema(model, key):
    properties = DEFINITIONS["pm.config.system." + key]["properties"]
    for api_name, schema in properties.items():
        value = example(schema)
        obj = model.model_validate({api_name: value})
        payload = obj.model_dump(by_alias=True, exclude_none=True)
        assert payload == {api_name: value}, api_name
        python_name = api_name.replace("-", "_")
        assert model(**{python_name: value}).model_dump(by_alias=True, exclude_none=True) == payload
        assert model(**{api_name: None}).model_dump(by_alias=True, exclude_none=True) == {}


@pytest.mark.parametrize("model", [SystemAdmin, DeviceZone])
def test_admin_and_zone_partial_get(client, post, model):
    request = model(device="FG01")
    post.return_value = {"data": {"name": "example"}, "status": {"code": 0}}
    obj = resolve(client.get(request)).first()
    assert obj.name == "example"
    assert obj.model_dump(by_alias=True, exclude_none=True) == {"name": "example"}


def test_zone_add_uses_structured_tags_and_excludes_metadata(client, post):
    post.return_value = {"status": {"code": 0}}
    tags = [{"name": "example", "category": ["example"], "tags": ["tag1"]}]
    obj = DeviceZone(device="FG01", name="zone1", oid=42, tagging=tags)
    assert resolve(client.add(obj)).success
    request = post.call_args.kwargs["request"]["params"][0]
    assert request["data"] == {"name": "zone1", "tagging": tags}


def test_admin_add_uses_password_alias_and_vdom_names(client, post):
    post.return_value = {"status": {"code": 0}}
    obj = SystemAdmin(device="FG01", name="example", old_password=["test-only"], vdom=VDOM(name="root"))
    assert resolve(client.add(obj)).success
    request = post.call_args.kwargs["request"]["params"][0]
    assert request["data"] == {"name": "example", "old-password": ["test-only"], "vdom": ["root"]}
    assert "test-only" not in repr(obj)


@pytest.mark.parametrize(
    "query, expected_url",
    [
        (DeviceInterface(device="FG01"), "/pm/config/device/FG01/global/system/interface/returned"),
        (SystemAdmin(device="FG01"), "/pm/config/device/FG01/global/system/admin/returned"),
        (DeviceZone(device="FG01", vdom="custom"), "/pm/config/device/FG01/vdom/custom/system/zone/returned"),
    ],
)
def test_returned_system_objects_retain_write_url_context(client, post, query, expected_url):
    post.return_value = {"data": [{"name": "returned"}], "status": {"code": 0}}
    obj = resolve(client.get(query)).first()
    assert obj.device == "FG01"
    assert obj.get_url(method="update") == expected_url
    assert obj.model_dump(by_alias=True, exclude_none=True) == {"name": "returned"}
    post.return_value = {"status": {"code": 0}}
    assert resolve(obj.update()).success
    outgoing = post.call_args.kwargs["request"]["params"][0]
    assert outgoing == {"url": expected_url, "data": {"name": "returned"}}


def test_get_does_not_copy_interface_selector_or_config_filters(client, post):
    request = DeviceInterface(device="FG01", fmg_interface="selected", alias="filter")
    post.return_value = {"data": [{"name": "returned"}], "status": {"code": 0}}
    obj = resolve(client.get(request)).first()
    assert obj.device == "FG01"
    assert obj.fmg_interface is None
    assert obj.alias is None
    assert obj.get_url(method="update").endswith("/returned")
