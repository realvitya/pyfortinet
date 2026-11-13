"""Install operations need a real device baseline; object deletion cannot undo them."""

import pytest

from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.securityconsole import InstallDeviceTask


@pytest.mark.requires_baseline
@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_install_device(self, fmg, lab_device):
        assert any(vdom.name == "root" for vdom in lab_device.vdom)
        task = fmg.get_obj(
            InstallDeviceTask,
            adom=fmg.adom,
            scope=[Scope(name=lab_device.name, vdom="root")],
            flags=["auto_lock_ws"],
        )
        result = task.exec()
        result.wait_for_task()
        assert result.success
