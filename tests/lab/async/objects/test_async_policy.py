"""Read-only checks against the lab's default policy package (PP)."""

from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.policy import Policy, PolicyPackage
from tests.lab.fixtures import AsyncTestCase


class TestObjectsOnLab(AsyncTestCase):
    async def test_policy_package_ops(self, fmg):
        assert await fmg.get(PolicyPackage, F(name="default"))

    async def test_policy_ops(self, fmg):
        assert await fmg.get(Policy(pkg="default"))
