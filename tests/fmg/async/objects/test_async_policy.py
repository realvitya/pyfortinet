"""Read-only checks against the lab's default policy package (PP)."""

from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.policy import Policy, PolicyPackage
from tests.conftest import AsyncTestCase


class TestPolicy:
    def test_policy_create(self):
        assert Policy(name="unassigned_policy").name == "unassigned_policy"


class TestObjectsOnLab(AsyncTestCase):
    async def test_policy_package_ops(self, fmg):
        assert await fmg.get(PolicyPackage, F(name="default"))

    async def test_policy_ops(self, fmg):
        assert await fmg.get(Policy(pkg="default"))
