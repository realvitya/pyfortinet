"""Normalized interface tests own only their generated objects."""

from pyfortinet.fmg_api.dynamic import NormalizedInterface
from tests.lab.fixtures import AsyncTestCase


class TestObjectsOnLab(AsyncTestCase):
    async def test_interface_ops(self, fmg, lab):
        assert await fmg.get(NormalizedInterface(name="port1", default_mapping="disable"))
        interface = await lab.object(NormalizedInterface, "intf", default_mapping="enable", defmap_intf="port1")
        assert await interface.add()
