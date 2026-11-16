"""Optional collection serializers distinguish absent values from empty lists."""

import json

import pytest

from pyfortinet.fmg_api.firewall import Address, AddressGroup, ServiceCategory, ServiceCustom, ServiceGroup
from pyfortinet.fmg_api.policy import Policy


@pytest.mark.parametrize(
    "model, fields",
    [
        (AddressGroup, ["member", "exclude_member"]),
        (ServiceGroup, ["member"]),
        (Policy, ["srcaddr", "dstaddr", "service"]),
        (ServiceCustom, ["category", "tcp_portrange", "udp_portrange", "sctp_portrange"]),
    ],
)
def test_optional_collections_preserve_none_and_empty(model, fields):
    empty = model()
    for payload in [empty.model_dump(), json.loads(empty.model_dump_json())]:
        assert all(payload[field] is None for field in fields)
    cleared = model(**{field: [] for field in fields})
    assert all(cleared.model_dump()[field] == [] for field in fields)
    assert all(field not in empty.model_dump(exclude_none=True) for field in fields)


@pytest.mark.parametrize(
    "model, field, member",
    [
        (AddressGroup, "member", Address(name="first")),
        (ServiceGroup, "member", ServiceCustom(name="first")),
        (Policy, "srcaddr", Address(name="first")),
        (ServiceCustom, "category", ServiceCategory(name="first")),
    ],
)
def test_reference_serializers_keep_member_names(model, field, member):
    obj = model(**{field: [member, "second"]})
    assert obj.model_dump()[field] == ["first", "second"]
