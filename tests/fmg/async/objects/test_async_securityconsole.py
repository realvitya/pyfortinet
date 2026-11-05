"""Install operations need a real device baseline; object deletion cannot undo them."""

import pytest

from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.securityconsole import InstallDeviceTask
from tests.conftest import AsyncTestCase


@pytest.mark.requires_baseline
class TestObjectsOnLab(AsyncTestCase):
    async def test_install_device(self, fmg, lab_device):
        assert any(vdom.name == "root" for vdom in lab_device.vdom)
        task = fmg.get_obj(
            InstallDeviceTask,
            adom=fmg.adom,
            scope=[Scope(name=lab_device.name, vdom="root")],
            flags=["auto_lock_ws"],
        )
        result = await task.exec()
        await result.wait_for_task()
        assert result.success
