"""Test of human API"""

import pytest
from pyfortinet.fmg_api.dynamic import NormalizedInterface

from pyfortinet import AsyncFMG
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.firewall import Address, AddressGroup, ServiceCustom, PortRange
from pyfortinet.fmg_api.policy import Policy, PolicyPackage
from pyfortinet.fmg_api.system import DeviceInterface, DeviceZone
from tests.conftest import AsyncTestCase


class TestInterface:
    def test_interface_create(self):
        iface = NormalizedInterface(name="inside")


@pytest.mark.usefixtures("fmg")
@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_interface_ops(self, fmg):
        inside_iface = fmg.get_obj(DeviceInterface, name="port1")
        ifaces = fmg.get(NormalizedInterface(name="port1")).data
        assert ifaces
