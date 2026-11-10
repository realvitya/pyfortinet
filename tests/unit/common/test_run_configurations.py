"""Shared IDE configurations keep offline and lab targets separate."""

import json
from pathlib import Path
from xml.etree import ElementTree

import pytest

ROOT = Path(__file__).resolve().parents[3]
CONFIGURATIONS = sorted((ROOT / ".run").glob("*.run.xml"))


@pytest.mark.parametrize("path", CONFIGURATIONS, ids=lambda path: path.stem)
def test_run_configuration_targets_and_scope(path):
    configuration = ElementTree.parse(path).getroot().find("configuration")
    options = {item.get("name"): item.get("value") for item in configuration.findall("option")}
    target = json.loads(options["_new_target"])
    arguments = json.loads(options["_new_additionalArguments"])
    assert options["WORKING_DIRECTORY"] == "$PROJECT_DIR$"
    assert json.loads(options["_new_targetType"]) == "PATH"
    relative_target = target.removeprefix("$PROJECT_DIR$/")
    assert (ROOT / relative_target).exists()
    assert options["IS_MODULE_SDK"] == "true"
    if relative_target.startswith("tests/lab"):
        assert "--lab_config private/lab-config.yml" in arguments
        assert "--run-baseline-tests" not in arguments
    else:
        assert relative_target.startswith(("tests/unit", "tests/transport"))
        assert "--lab_config" not in arguments
        assert "tests/lab" not in arguments


def test_shared_configuration_set_is_present():
    assert CONFIGURATIONS
    assert (ROOT / ".run/offline_all.run.xml").is_file()
    assert (ROOT / ".run/lab_all.run.xml").is_file()
