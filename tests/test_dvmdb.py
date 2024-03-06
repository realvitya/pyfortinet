"""Test of human API"""
import pytest
from pyfortinet import FMG, FMGSettings
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmbd import Device
from pyfortinet.fmg_api.dvmcmd import ModelDevice, DeviceTask


need_lab = pytest.mark.skipif(not pytest.lab_config, reason=f"Lab config {pytest.lab_config_file} does not exist!")


@need_lab
class TestObjectsOnLab:
    fmg = FMG(FMGSettings(**pytest.lab_config.get("fmg"))).open()
    fmg_connected = pytest.mark.skipif(
        not fmg._token, reason=f"FMG {pytest.lab_config.get('fmg', {}).get('base_url')} is not connected!"
    )

    @fmg_connected
    def test_dvmdb_device(self):
        device = ModelDevice(name="TEST-DEVICE", sn="FG100FTK22345678", os_ver="7.0", mr=2)
        job = DeviceTask(adom=self.fmg.adom, device=device)
        result = self.fmg.exec(job)
        result.wait_for_task()
        assert result.success
        job = DeviceTask(adom=self.fmg.adom, device=device, action="del")
        result = self.fmg.exec(job)
        assert result
        result = self.fmg.get(Device, F(name__like="TEST%"))
        assert result

    @fmg_connected
    def test_close_fmg(self):
        self.fmg.close(discard_changes=True)
