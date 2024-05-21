"""Test of DVMDB object operations"""

import pytest
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device, ADOM
from pyfortinet.fmg_api.dvmcmd import ModelDevice, DeviceTask


@pytest.mark.usefixtures("fmg")
@pytest.mark.filterwarnings("ignore:Unverified")
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

    def test_dvmdb_adom(self, fmg):
        root_adom = fmg.get(ADOM, F(name="root")).first()
        test_adom = fmg.get(ADOM, F(name="test-adom")).first()
        if not test_adom:
            test_adom = fmg.get_obj(ADOM(name="test-adom"))
            test_adom.add()
        result = fmg.get(ADOM, F(name="clone-adom"))
        if result.first():
            fmg.delete(ADOM(name="clone-adom"))
        result = test_adom.clone(create_task=True, name="clone-adom")
        result.wait_for_task(callback=lambda percent, log: print(f"Task at {percent}%: {log}"))
        assert result
        clone_adom = fmg.get(ADOM, F(name="clone-adom")).first()
        result = clone_adom.delete()
        assert result
        result = test_adom.delete()
        assert result
