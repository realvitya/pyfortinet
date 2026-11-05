"""Device settings tests use FG01 and remove their generated configuration."""

from pyfortinet.fmg_api.system import DeviceInterface, DeviceZone, SystemAdmin
from tests.conftest import AsyncTestCase


class TestInterface:
    def test_interface_create(self):
        assert DeviceInterface(name="inside").name == "inside"


class TestObjectsOnLab(AsyncTestCase):
    async def test_interface_ops(self, fmg, lab_device):
        assert await fmg.get(DeviceInterface(device=lab_device.name))

    async def test_zone_ops(self, fmg, lab, lab_device):
        interface = await lab.object(
            DeviceInterface, "vlan", device=lab_device.name, type="vlan", interface="port1", vlanid=123
        )
        assert await interface.add()
        zone = await lab.object(DeviceZone, "zone", device=lab_device.name, interface=[interface])
        assert await zone.add()
        assert await fmg.get(DeviceZone(device=lab_device.name, name=zone.name))

    async def test_sysadmin_ops(self, fmg, lab, lab_device):
        user = await lab.object(
            SystemAdmin, "admin", device=lab_device.name, password="test-only-password", accprofile="super_admin"
        )
        assert await user.set()
        await user.refresh()
        assert user.accprofile in ("super_admin", ["super_admin"])
        user.accprofile = "prof_admin"
        assert await user.update()
        await user.refresh()
        assert user.accprofile in ("prof_admin", ["prof_admin"])
