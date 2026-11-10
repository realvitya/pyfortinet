"""Device and ADOM lifecycle tests own unique resources and await task completion."""

from uuid import uuid4

import pytest

from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmcmd import DeviceTask
from pyfortinet.fmg_api.dvmdb import ADOM, VDOM, Device


@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_dvmdb_device(self, fmg, lab):
        device = fmg.get_obj(
            Device, name=lab.name("device"), sn="FG100FTK" + uuid4().hex[:8].upper(), os_ver="7.0", mr=2
        )
        device.fmg_scope = fmg.adom
        lab.reserve(
            device.get_url(method="delete"),
            delete=lambda: fmg.exec(DeviceTask(adom=fmg.adom, device=device, action="del")),
        )
        result = fmg.exec(DeviceTask(adom=fmg.adom, device=device))
        lab.wait(result)
        assert result.success
        assert fmg.get(VDOM(device=device.name, name="root"))
        assert (fmg.get(Device, F(name=device.name))).first() is not None
        result = fmg.exec(DeviceTask(adom=fmg.adom, device=device, action="del"))
        lab.wait(result)
        assert (fmg.get(Device, F(name=device.name))).first() is None

    def test_dvmdb_adom(self, fmg, lab):
        source = lab.object(ADOM, "adom")
        clone = lab.object(ADOM, "clone")
        assert source.add()
        result = source.clone(create_task=True, name=clone.name)
        lab.wait(result)
        assert result.success
        assert (fmg.get(ADOM, F(name=clone.name))).first() is not None
        assert clone.delete()
        assert source.delete()
