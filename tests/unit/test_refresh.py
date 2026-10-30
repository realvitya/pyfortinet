"""Refreshing objects retains their routing context."""

import pytest

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.firewall import Address
from pyfortinet.fmg_api.policy import Policy

from .conftest import resolve


@pytest.mark.parametrize("policy", [False, True])
def test_refresh_retains_identity_and_scope(client, post, policy):
    """Refresh the original target and preserve URL-only parameters."""
    if policy:
        obj = Policy(policyid=42, pkg="package", adom="other", name="before", fmg_scope="other")
        data = {"policyid": 42, "name": "after"}
        url = "/pm/config/adom/other/pkg/package/firewall/policy/42"
    else:
        obj = Address(name="example", comment="before", fmg_scope="other")
        data = {"name": "example", "comment": "after"}
        url = "/pm/config/adom/other/obj/firewall/address/example"
    post.return_value = {"data": data}
    result = resolve(client.refresh(obj))
    assert result is obj
    assert post.call_args.kwargs["request"]["params"][0]["url"] == url
    assert obj.fmg_scope == "adom/other"
    assert (obj.name if policy else obj.comment) == "after"
    assert obj.get_url() == url


def test_refresh_ignores_extra_response_attributes(client, post):
    """Models permitting extras should refresh without treating extras as fields."""

    class ExtensibleAddress(Address):
        model_config = {"extra": "allow"}

    obj = ExtensibleAddress(name="example", custom="value", fmg_scope="other")
    post.return_value = {"data": {"name": "example", "comment": "after"}}
    assert resolve(client.refresh(obj)) is obj
    assert obj.comment == "after"
    assert isinstance(obj, FMGObject)
