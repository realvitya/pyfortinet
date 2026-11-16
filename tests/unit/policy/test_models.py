"""Offline model checks moved out of the lab tree."""

from pyfortinet.fmg_api.policy import PackageSettings, Policy, PolicyPackage


def test_package_inspection_mode_uses_api_key():
    settings = PackageSettings(**{"inspection-mode": "flow"})
    package = PolicyPackage(name="example", package_settings=settings)
    payload = package.model_dump(by_alias=True, exclude_none=True)
    assert payload["package settings"] == {"inspection-mode": "flow"}


class TestAsyncPolicy:
    def test_policy_create(self):
        assert Policy(name="unassigned_policy").name == "unassigned_policy"


class TestSyncPolicy:
    def test_policy_create(self):
        assert Policy(name="unassigned_policy").name == "unassigned_policy"
