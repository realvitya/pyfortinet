"""Dynamic mapping URL contracts used by high-level operations."""

import pytest

from pyfortinet.exceptions import FMGException
from pyfortinet.fmg_api._requests import prepare_get
from pyfortinet.fmg_api.dynamic import DynamicMapping, PlatformMapping


@pytest.mark.parametrize("method", ["get", "add", "set", "update", "delete"])
@pytest.mark.parametrize("selected", [False, True])
def test_platform_mapping_urls(method, selected):
    obj = PlatformMapping(interface="inside", platform_mapping="FortiGate" if selected else None, fmg_scope="root")
    suffix = "/FortiGate" if selected else ""
    assert obj.get_url(method) == f"/pm/config/adom/root/obj/dynamic/interface/inside/platform_mapping{suffix}"


@pytest.mark.parametrize("method", ["get", "add", "set", "update", "delete"])
@pytest.mark.parametrize("selected", [False, True])
def test_dynamic_mapping_urls(method, selected):
    obj = DynamicMapping(
        interface="inside",
        dynamic_mapping_name="FGT1" if selected else None,
        dynamic_mapping_vdom="root" if selected else None,
        fmg_scope="root",
    )
    suffix = "/FGT1/root" if selected else ""
    assert obj.get_url(method) == f"/pm/config/adom/root/obj/dynamic/interface/inside/dynamic_mapping{suffix}"


@pytest.mark.parametrize("fields", [{"dynamic_mapping_name": "FGT1"}, {"dynamic_mapping_vdom": "root"}])
def test_dynamic_mapping_rejects_partial_identity(fields):
    with pytest.raises(FMGException, match="both are required"):
        DynamicMapping(interface="inside", fmg_scope="root", **fields).get_url()


def test_platform_mapping_parent_selectors_are_not_api_filters():
    request = PlatformMapping(interface="inside", platform_mapping="FortiGate")
    parameters, _ = prepare_get(request, "root")
    assert parameters == {
        "url": "/pm/config/adom/root/obj/dynamic/interface/inside/platform_mapping/FortiGate",
        "loadsub": 1,
    }
