"""Test of DVMDB object operations"""

import asyncio
import pytest

from pyfortinet import AsyncFMG
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device, ADOM, VDOM
from pyfortinet.fmg_api.dvmcmd import DeviceTask

from tests.conftest import AsyncTestCase


class TestObjectsOnLab(AsyncTestCase):
    @staticmethod
    async def async_callback(percent: int, log: str):
        """Async test callback"""
        print(f"Task at {percent}%: {log}")
        await asyncio.sleep(0.1)

    async def test_dvmdb_device(self, fmg: AsyncFMG):
        # test adding device
        device = Device(name="TEST-DEVICE", sn="FG100FTK22345678", os_ver="7.0", mr=2)
        job = DeviceTask(adom=fmg.adom, device=device)
        result = await fmg.exec(job)
        await result.wait_for_task(callback=lambda percent, log: print(f"{percent}% - {log}"))
        assert result.success
        # test VDOM
        result = await fmg.get(VDOM(device="TEST-DEVICE", name="root"))
        assert result
        # test Device
        result = await fmg.get(Device(conn_status="UNKNOWN"))
        assert result.data  # should be at least the previously created device
        # test removing device
        job = DeviceTask(adom=fmg.adom, device=device, action="del")
        result = await fmg.exec(job)
        assert result
        result = await fmg.get(Device, F(name__like="TEST%"))
        assert result

    async def test_dvmdb_adom(self, fmg: AsyncFMG):
        root_adom = (await fmg.get(ADOM, F(name="root"))).first()
        test_adom = (await fmg.get(ADOM, F(name="test-adom"))).first()
        if not test_adom:
            test_adom = fmg.get_obj(ADOM(name="test-adom"))
            await test_adom.add()
        result = await fmg.get(ADOM, F(name="clone-adom"))
        if result.first():
            await fmg.delete(ADOM(name="clone-adom"))
        result = await test_adom.clone(create_task=True, name="clone-adom")
        await result.wait_for_task(callback=self.async_callback)
        assert result
        clone_adom = (await fmg.get(ADOM, F(name="clone-adom"))).first()
        result = await clone_adom.delete()
        assert result
        result = await test_adom.delete()
        assert result
