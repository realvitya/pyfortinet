"""Shared IDE configurations keep offline and lab targets separate."""

import json
import re
import shlex
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
    argument_tokens = shlex.split(arguments)
    assert options["WORKING_DIRECTORY"] == "$PROJECT_DIR$"
    assert json.loads(options["_new_targetType"]) == "PATH"
    relative_target = target.removeprefix("$PROJECT_DIR$/")
    assert (ROOT / relative_target).exists()
    assert options["IS_MODULE_SDK"] == "true"
    if relative_target.startswith("tests/lab"):
        assert "--lab_config private/lab-config.yml" in arguments
        if "--run-baseline-tests" in argument_tokens:
            assert re.search(r"\bbaseline\b", configuration.get("name", ""), re.IGNORECASE), (
                "Configurations enabling baseline tests must say baseline in their display name"
            )
    else:
        assert relative_target.startswith(("tests/unit", "tests/transport"))
        assert "--lab_config" not in arguments
        assert "tests/lab" not in arguments
        assert "--run-baseline-tests" not in argument_tokens


def test_shared_configuration_set_is_present():
    assert CONFIGURATIONS
    targets = []
    for path in CONFIGURATIONS:
        configuration = ElementTree.parse(path).getroot().find("configuration")
        options = {item.get("name"): item.get("value") for item in configuration.findall("option")}
        target = json.loads(options["_new_target"])
        arguments = shlex.split(json.loads(options["_new_additionalArguments"]))
        targets.append((target, arguments))
    assert any(target == "$PROJECT_DIR$/tests/unit" for target, _ in targets)
    assert any(
        target == "$PROJECT_DIR$/tests/lab" and "--run-baseline-tests" not in arguments for target, arguments in targets
    )
