"""Shared data and assertions for the synchronous and asynchronous firewall lab tests."""

from typing import NamedTuple, Optional

import pytest

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.firewall import (
    VIP,
    IPPool,
    IPPoolDynamicMapping,
    IPPoolGroup,
    ProxyAddress,
    ProxyAddressGroup,
    VIPDynamicMapping,
)


class ObjectCase(NamedTuple):
    model: type[FMGObject]
    fields: dict[str, object]
    comment_field: str


class GroupCase(NamedTuple):
    model: type[FMGObject]
    member_model: type[FMGObject]
    member_fields: tuple[dict[str, object], dict[str, object]]
    group_fields: dict[str, object]
    comment_field: str
    clone_error: Optional[str] = None


class MappingCase(NamedTuple):
    parent: ObjectCase
    mapping_model: type
    overrides: dict[str, object]
    field: str
    changed_value: object


PROXY = ObjectCase(ProxyAddress, {"type": "host-regex", "host_regex": r"^example\.invalid$"}, "comment")
VIP_CASE = ObjectCase(
    VIP,
    {"extintf": ["any"], "extip": ["203.0.113.10"], "mappedip": ["192.0.2.10"], "arp_reply": "disable"},
    "comment",
)
POOL = ObjectCase(
    IPPool,
    {"type": "overload", "startip": "203.0.113.10", "endip": "203.0.113.19", "arp_reply": "disable"},
    "comments",
)
CGN_POOL_FIELDS = {**POOL.fields, "type": "cgn-resource-allocation"}

OBJECT_CASES = [pytest.param(case, id=case.model.__name__) for case in (PROXY, VIP_CASE, POOL)]
GROUP_CASES = [
    pytest.param(
        GroupCase(ProxyAddressGroup, ProxyAddress, (PROXY.fields, PROXY.fields), {"type": "dst"}, "comment"),
        id="ProxyAddressGroup",
    ),
    pytest.param(
        GroupCase(
            IPPoolGroup,
            IPPool,
            (CGN_POOL_FIELDS, {**CGN_POOL_FIELDS, "startip": "203.0.113.20", "endip": "203.0.113.29"}),
            {},
            "comments",
            "can not be used in another ippool_grp",
        ),
        id="IPPoolGroup",
    ),
]
MAPPING_CASES = [
    pytest.param(
        MappingCase(
            VIP_CASE,
            VIPDynamicMapping,
            {"extintf": "port1", "extip": ["203.0.113.30"], "mappedip": ["192.0.2.30"]},
            "mappedip",
            ["192.0.2.31"],
        ),
        id="VIP",
    ),
    pytest.param(
        MappingCase(
            POOL,
            IPPoolDynamicMapping,
            {"startip": "203.0.113.30", "endip": "203.0.113.39"},
            "endip",
            "203.0.113.40",
        ),
        id="IPPool",
    ),
]


def require_test_adom(adom: str) -> None:
    """Refuse writes outside the lab target authorized in AGENTS.md."""
    assert adom == "test", "These lab scenarios require the authorized ADOM test"


def assert_fields(obj: FMGObject, expected: dict[str, object]) -> None:
    """Check selected configuration without depending on device-specific default fields."""
    assert obj is not None
    for field, value in expected.items():
        assert getattr(obj, field) == value, field


def assert_mapping(obj: FMGObject, case: MappingCase, expected: dict[str, object]) -> None:
    """Check a typed mapping, its exact device/VDOM scope, and its override values."""
    assert obj.dynamic_mapping is not None
    assert len(obj.dynamic_mapping) == 1
    mapping = obj.dynamic_mapping[0]
    assert isinstance(mapping, case.mapping_model)
    assert [(scope.name, scope.vdom) for scope in mapping.mapping__scope] == [("FG01", "root")]
    for field, value in expected.items():
        assert getattr(mapping, field) == value, field
