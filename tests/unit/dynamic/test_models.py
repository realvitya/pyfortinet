"""Offline model checks moved out of the lab tree."""

import pytest

from pyfortinet.fmg_api.dynamic import NormalizedInterface
from tests.unit.conftest import resolve


@pytest.mark.parametrize("key", ["zone-only", "zone_only"])
@pytest.mark.parametrize("value", ["enable", "disable", None])
def test_zone_only_aliases_round_trip(key, value):
    obj = NormalizedInterface(**{key: value})
    assert obj.zone_only == value
    payload = obj.model_dump(by_alias=True, exclude_none=True)
    assert payload == ({"zone-only": value} if value is not None else {})
    assert NormalizedInterface.model_validate(payload).zone_only == value
    assert NormalizedInterface.model_validate_json(obj.model_dump_json(by_alias=True)).zone_only == value


@pytest.mark.parametrize("key", ["wildcard-intf", "wildcard_intf"])
@pytest.mark.parametrize("value", ["port*", "", None])
def test_wildcard_interface_aliases_round_trip(key, value):
    obj = NormalizedInterface(**{key: value})
    assert obj.wildcard_intf == value
    payload = obj.model_dump(by_alias=True, exclude_none=True)
    assert payload == ({"wildcard-intf": value} if value is not None else {})
    assert NormalizedInterface.model_validate(payload).wildcard_intf == value
    assert NormalizedInterface.model_validate_json(obj.model_dump_json(by_alias=True)).wildcard_intf == value


@pytest.mark.parametrize("method", ["add", "set", "update"])
def test_wildcard_and_zone_only_write_independent_fields(client, post, method):
    post.return_value = {"status": {"code": 0}}
    obj = NormalizedInterface(name="inside", wildcard="enable", wildcard_intf="port*", zone_only="disable")
    assert resolve(getattr(client, method)(obj)).success
    parameters = post.call_args.kwargs["request"]["params"][0]
    assert parameters["data"] == {
        "name": "inside",
        "wildcard": "enable",
        "wildcard-intf": "port*",
        "zone-only": "disable",
    }


class TestAsyncInterface:
    def test_interface_create(self):
        assert NormalizedInterface(name="inside").name == "inside"


class TestSyncInterface:
    def test_interface_create(self):
        assert NormalizedInterface(name="inside").name == "inside"
