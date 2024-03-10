"""Test of human API"""
from pyfortinet import AsyncFMG
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.dvmcmd import ModelDevice, DeviceTask
from pyfortinet.fmg_api.firewall import Address
from tests.conftest import AsyncTestCase


class TestObjectsOnLab(AsyncTestCase):
    async def test_dvmdb_device(self, fmg: AsyncFMG):
        device = fmg.get_obj(ModelDevice, name="TEST-DEVICE", sn="FG100FTK22345678", os_ver="7.0", mr=2)
        job = DeviceTask(adom=fmg.adom, device=device)
        result = await fmg.exec(job)
        await result.wait_for_task()
        assert result.success
        job = DeviceTask(adom=fmg.adom, device=device, action="del")
        result = await fmg.exec(job)
        assert result
        result = await fmg.get(Device, F(name__like="TEST%"))
        assert result

    async def test_object_functions(self, fmg: AsyncFMG):
        to_add = fmg.get_obj(Address, name="test-firewall-address", subnet="10.0.0.0/24")
        # test ADD
        result = await to_add.add()
        assert result
        # test GET
        address = (await fmg.get(Address, F(name__like="test-firewall-addr%"))).first()
        assert address.name == "test-firewall-address"
        address.subnet = "10.0.1.0/24"
        # test UPDATE
        result = await address.update()
        assert result
        address = (await fmg.get(Address, F(name=address.name))).first()
        assert address.subnet == "10.0.1.0/24"
        # test DELETE
        result = await address.delete()
        assert result
        result = await fmg.get(Address, F(name="test-firewall-address"))
        assert result and not result.data  # ensure empty result
        # test SET
        result = await to_add.set()
        assert result
        result = await to_add.delete()
        assert result
        result = await fmg.get(Address, F(name="test-firewall-address"))
        assert result and not result.data  # ensure empty result
