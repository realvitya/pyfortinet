"""Read-only checks against the lab's default policy package (PP)."""

import pytest

from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.policy import Policy, PolicyPackage


class TestPolicy:
    def test_policy_create(self):
        assert Policy(name="unassigned_policy").name == "unassigned_policy"


@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_policy_package_ops(self, fmg):
        assert fmg.get(PolicyPackage, F(name="default"))

    def test_policy_ops(self, fmg):
        assert fmg.get(Policy(pkg="default"))
