"""Test of human API"""

import pytest

from pyfortinet.fmg_api.system import DeviceInterface, DeviceZone, SystemAdmin
from pyfortinet.fmg_api.dvmdb import Device


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

    def test_sysadmin_ops(self, fmg):
        my_fw = fmg.get(Device).first()
        test_user = fmg.get_obj(SystemAdmin(device=my_fw.name, name="test-admin", password="verysecret", accprofile="super_admin"))
        test_user.set()
        test_user.refresh()
        old_profile = test_user.accprofile
        test_user.accprofile = "prof_admin"
        test_user.update()
        test_user.refresh()
        assert old_profile != test_user.accprofile
