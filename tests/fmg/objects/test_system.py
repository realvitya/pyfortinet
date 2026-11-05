"""Device settings tests use FG01 and remove their generated configuration."""

import pytest

from pyfortinet.fmg_api.system import DeviceInterface, DeviceZone, SystemAdmin


class TestInterface:
    def test_interface_create(self):
        assert DeviceInterface(name="inside").name == "inside"


@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_interface_ops(self, fmg, lab_device):
        assert fmg.get(DeviceInterface(device=lab_device.name))

    def test_zone_ops(self, fmg, lab, lab_device):
        interface = lab.object(
            DeviceInterface, "vlan", device=lab_device.name, type="vlan", interface="port1", vlanid=123
        )
        assert interface.add()
        zone = lab.object(DeviceZone, "zone", device=lab_device.name, interface=[interface])
        assert zone.add()
        assert fmg.get(DeviceZone(device=lab_device.name, name=zone.name))

    def test_sysadmin_ops(self, fmg, lab, lab_device):
        user = lab.object(
            SystemAdmin, "admin", device=lab_device.name, password="test-only-password", accprofile="super_admin"
        )
        assert user.set()
        user.refresh()
        assert user.accprofile in ("super_admin", ["super_admin"])
        user.accprofile = "prof_admin"
        assert user.update()
        user.refresh()
        assert user.accprofile in ("prof_admin", ["prof_admin"])
