"""Offline model checks moved out of the lab tree."""

import pytest

from pyfortinet.fmg_api.dvmdb import VDOM, Device
from pyfortinet.fmg_api.system import DeviceInterface, DeviceZone


@pytest.mark.parametrize("objects", [False, True])
def test_zone_url_uses_device_and_vdom_names(objects):
    device = Device(name="FGT1") if objects else "FGT1"
    vdom = VDOM(name="root") if objects else "root"
    zone = DeviceZone(device=device, vdom=vdom, name="inside")
    assert zone.get_url("update") == "/pm/config/device/FGT1/vdom/root/system/zone/inside"
    assert zone.device is device
    assert zone.vdom is vdom


class TestAsyncInterface:
    def test_interface_create(self):
        assert DeviceInterface(name="inside").name == "inside"


class TestSyncInterface:
    def test_interface_create(self):
        assert DeviceInterface(name="inside").name == "inside"
