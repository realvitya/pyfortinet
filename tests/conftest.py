"""Shared pytest options; lab connections are confined to tests/lab."""

import pytest


def pytest_addoption(parser):
    parser.addoption("--lab_config", action="store", default="lab-config.yml")
    parser.addoption(
        "--run-baseline-tests", action="store_true", help="Run install tests requiring an authorized snapshot restore"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "requires_baseline: installs configuration; requires snapshot-based restoration")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-baseline-tests"):
        skip = pytest.mark.skip(reason="Requires an authorized baseline restore and --run-baseline-tests")
        for item in items:
            if item.get_closest_marker("requires_baseline"):
                item.add_marker(skip)
