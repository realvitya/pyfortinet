"""Load lab credentials only when the lab tree is selected."""

from pathlib import Path

import pytest
from ruamel.yaml import YAML

from .fixtures import base_lab, fmg, fmg_base, lab, lab_device

__all__ = ["base_lab", "fmg", "fmg_base", "lab", "lab_device"]


def pytest_configure(config):
    pytest.lab_config_file = Path(config.getoption("--lab_config"))
    pytest.lab_config = {}
    if pytest.lab_config_file.is_file():
        pytest.lab_config = YAML(typ="safe", pure=True).load(pytest.lab_config_file) or {}
