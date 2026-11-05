"""Device and ADOM lifecycle tests own unique resources and await task completion."""

from uuid import uuid4

from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmcmd import DeviceTask
from pyfortinet.fmg_api.dvmdb import ADOM, VDOM, Device
from tests.conftest import AsyncTestCase


class TestObjectsOnLab(AsyncTestCase):
    async def test_dvmdb_device(self, fmg, lab):
        device = fmg.get_obj(
            Device, name=lab.name("device"), sn="FG100FTK" + uuid4().hex[:8].upper(), os_ver="7.0", mr=2
        )
        device.fmg_scope = fmg.adom
        await lab.reserve(
            device.get_url(method="delete"),
            delete=lambda: fmg.exec(DeviceTask(adom=fmg.adom, device=device, action="del")),
        )
        result = await fmg.exec(DeviceTask(adom=fmg.adom, device=device))
        await lab.wait(result)
        assert result.success
        assert await fmg.get(VDOM(device=device.name, name="root"))
        assert (await fmg.get(Device, F(name=device.name))).first() is not None
        result = await fmg.exec(DeviceTask(adom=fmg.adom, device=device, action="del"))
        await lab.wait(result)
        assert (await fmg.get(Device, F(name=device.name))).first() is None

    async def test_dvmdb_adom(self, fmg, lab):
        source = await lab.object(ADOM, "adom")
        clone = await lab.object(ADOM, "clone")
        assert await source.add()
        result = await source.clone(create_task=True, name=clone.name)
        await lab.wait(result)
        assert result.success
        assert (await fmg.get(ADOM, F(name=clone.name))).first() is not None
        assert await clone.delete()
        assert await source.delete()
