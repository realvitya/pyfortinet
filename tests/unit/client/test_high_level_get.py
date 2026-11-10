"""High-level request and object scope regression tests."""

from copy import deepcopy

import pytest

from pyfortinet.fmg_api.firewall import Address
from tests.unit.conftest import resolve


@pytest.mark.parametrize("instance", [False, True])
@pytest.mark.parametrize("scope", [None, "other", "global", "adom/other"])
def test_get_retains_scope_and_fields(client, post, instance, scope):
    """Returned objects retain their source even after the client changes ADOM."""
    post.return_value = {"data": [{"name": "example"}], "status": {"code": 0}}
    request = Address() if instance else Address
    response = resolve(client.get(request, scope=scope, fields=["name"]))
    parameters = post.call_args.kwargs["request"]["params"][0]
    expected_scope = scope or "root"
    if expected_scope != "global" and not expected_scope.startswith("adom/"):
        expected_scope = f"adom/{expected_scope}"
    assert parameters["fields"] == ["name"]
    assert parameters["url"] == f"/pm/config/{expected_scope}/obj/firewall/address"
    address = response.first()
    assert address.fmg_scope == expected_scope
    assert address._fmg is client
    client.adom = "changed"
    assert address.get_url(method="update") == f"/pm/config/{expected_scope}/obj/firewall/address/example"


def test_instance_scope_takes_precedence(client, post):
    """An explicitly scoped object wins over request and connection defaults."""
    post.return_value = {"data": [{"name": "example"}]}
    address = Address(name="example", fmg_scope="original")
    result = resolve(client.get(address, scope="other", filters='name like "ex%"'))
    assert result.first().fmg_scope == "adom/original"
    assert post.call_args.kwargs["request"]["params"][0]["filter"]


@pytest.mark.parametrize("payload", [{"data": None}, {}, {"data": []}, {"data": {"name": "example"}}])
def test_get_handles_optional_data_without_mutating_response(client, post, payload):
    """Successful empty replies yield no objects; single objects are wrapped."""
    payload = {"status": {"code": 0}, **payload}
    original = deepcopy(payload)
    post.return_value = payload
    result = resolve(client.get(Address))
    assert result.success
    assert [address.name for address in result.data] == (["example"] if payload.get("data") else [])
    assert payload == original
