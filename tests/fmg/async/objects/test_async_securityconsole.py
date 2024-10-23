"""Test security console features"""

import re

import pytest
import random

from pyfortinet import FMGResponse
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.securityconsole import InstallDeviceTask


@pytest.mark.usefixtures("fmg")
@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_install_device(self, fmg):
        test_device: Device = fmg.get(Device).first()
        test_device.desc = (
            test_device.desc + "test: " + str(random.randint(1, 1000))
            if "test:" not in test_device.desc
            else re.sub(r"test: \d+", "test: " + str(random.randint(1, 1000)), test_device.desc)
        )
        test_device.update()

        vdom = test_device.vdom[0].name
        task: InstallDeviceTask = fmg.get_obj(
            InstallDeviceTask, adom=fmg.adom, scope=[Scope(name=test_device.name, vdom=vdom)], flags=["auto_lock_ws"]
        )
        # result = fmg.exec(task)
        result: FMGResponse = task.exec()
        result.wait_for_task(callback=lambda percent, log: print(f"Task at {percent}%: {log}"))
        assert result.success
