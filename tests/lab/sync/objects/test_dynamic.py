"""Normalized interface tests own only their generated objects."""

import pytest

from pyfortinet.fmg_api.dynamic import NormalizedInterface


@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_interface_ops(self, fmg, lab):
        assert fmg.get(NormalizedInterface(name="port1", default_mapping="disable"))
        interface = lab.object(NormalizedInterface, "intf", default_mapping="enable", defmap_intf="port1")
        assert interface.add()
