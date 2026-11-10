"""Offline model checks moved out of the lab tree."""

from pyfortinet.fmg_api.dynamic import NormalizedInterface


class TestAsyncInterface:
    def test_interface_create(self):
        assert NormalizedInterface(name="inside").name == "inside"


class TestSyncInterface:
    def test_interface_create(self):
        assert NormalizedInterface(name="inside").name == "inside"
