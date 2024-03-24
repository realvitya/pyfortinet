"""Test of DVMDB object operations"""

import pytest
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.dvmcmd import ModelDevice, DeviceTask


@pytest.mark.usefixtures("fmg")
class TestObjectsOnLab:
    def test_dvmdb_device(self, fmg):
        device = ModelDevice(name="TEST-DEVICE", sn="FG100FTK22345678", os_ver="7.0", mr=2)
        job = DeviceTask(adom=fmg.adom, device=device)
        result = fmg.exec(job)
        result.wait_for_task()
        assert result.success
        job = DeviceTask(adom=fmg.adom, device=device, action="del")
        result = fmg.exec(job)
        assert result
        result = fmg.get(Device, F(name__like="TEST%"))
        assert result
