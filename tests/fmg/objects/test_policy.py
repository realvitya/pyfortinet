"""Test of human API"""

import pytest

from pyfortinet import AsyncFMG
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.firewall import Address, AddressGroup, ServiceCustom, PortRange
from pyfortinet.fmg_api.policy import Policy, PolicyPackage
from tests.conftest import AsyncTestCase


class TestPolicy:
    def test_policy_create(self):
        unassigned_policy = Policy(name="unassigned_policy")


@pytest.mark.usefixtures("fmg")
@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_policy_package_ops(self, fmg):
        ppackages = fmg.get(PolicyPackage, F(name="default"))
        assert ppackages

    def test_policy_ops(self, fmg):
        policies = fmg.get(Policy(pkg="default")).data
        # assert policies
