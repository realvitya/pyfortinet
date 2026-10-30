"""High-level request and object scope regression tests."""

import pytest

from pyfortinet.fmg_api.firewall import Address

from .conftest import resolve


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
