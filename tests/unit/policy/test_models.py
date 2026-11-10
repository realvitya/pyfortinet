"""Offline model checks moved out of the lab tree."""

from pyfortinet.fmg_api.policy import Policy


class TestAsyncPolicy:
    def test_policy_create(self):
        assert Policy(name="unassigned_policy").name == "unassigned_policy"


class TestSyncPolicy:
    def test_policy_create(self):
        assert Policy(name="unassigned_policy").name == "unassigned_policy"
