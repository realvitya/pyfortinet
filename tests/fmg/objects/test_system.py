"""Test of human API"""

import pytest
from pyfortinet.fmg_api.system import DeviceInterface, DeviceZone

from pyfortinet import AsyncFMG
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.firewall import Address, AddressGroup, ServiceCustom, PortRange
from pyfortinet.fmg_api.policy import Policy, PolicyPackage
from tests.conftest import AsyncTestCase


class TestInterface:
    def test_interface_create(self):
        iface = DeviceInterface(name="inside")


@pytest.mark.usefixtures("fmg")
@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_interface_ops(self, fmg):
        # inside_iface = fmg.get_obj(DeviceInterface, device="FG01")
        ifaces = fmg.get(DeviceInterface(device="FG01"))
        assert ifaces

    def test_zone_ops(self, fmg):
        test_iface = fmg.get_obj(DeviceInterface(device="FG01", name="vlan_test", type="vlan", interface="port1", vlanid=123))
        test_iface.add()
        new_zone = fmg.get_obj(DeviceZone, device="FG01", name="test_inside", interface=[test_iface])
        response = new_zone.add()
        zones = fmg.get(DeviceZone(device="FG01"))
        assert zones
