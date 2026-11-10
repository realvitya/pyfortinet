"""Offline model checks moved out of the lab tree."""

from pyfortinet.fmg_api.system import DeviceInterface


class TestAsyncInterface:
    def test_interface_create(self):
        assert DeviceInterface(name="inside").name == "inside"


class TestSyncInterface:
    def test_interface_create(self):
        assert DeviceInterface(name="inside").name == "inside"
