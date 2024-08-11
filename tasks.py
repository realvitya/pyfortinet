"""Invoke task file"""

import shutil
from pathlib import Path
from typing import Literal, Optional

from invoke import task


@task()
def clean_dist(cmd):  # pylint: disable=unused-argument  # mandatory argument
    """Clean dist directory"""
    directory = Path("dist")
    if directory.is_dir():
        for item in directory.glob("*"):
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()
            print(f"{item} deleted")


@task(clean_dist)
def clean(cmd):  # pylint: disable=unused-argument  # mandatory argument
    """Clean packaging related stuff"""


@task(clean)
def build(cmd):
    """Build package"""
    cmd.run("flit build")


@task(
    help={
        "push_to_github": "Push to GitHub pages after building the docs",
    }
)
def mkdocs(cmd, push_to_github=False):
    """Compile docs"""
    cmd.run("mkdocs build")
    if push_to_github:
        cmd.run("mkdocs gh-deploy")


MODULES = Literal["async", "sync", "objects", "all"]


@task(
    help = {
        "module": f"Test only on modules from this list: {MODULES.__args__}",
        "verbose": "Print out all test function name",
    }
)
def test(cmd, module: MODULES = "all", verbose=False):
    """Run tests

    This function assumes that testing environment is configued in `private/lab-config.yml` and there is at least
    one firewall connected to the FMG.
    """
    dirs = {
        "async": "tests/fmg/async",
        "sync": "tests/fmg/test_*",
        "objects": "tests/fmg/objects",
    }
    test_target = dirs.get(module, "tests")
    cmd.run(f"pytest {'-vvv' if verbose else ''} --lab_config private/lab-config.yml {test_target}")


@task()
def mkdocs_serve(cmd):
    """Run built-in webserver for docs"""
    cmd.run("mkdocs serve")


LinterType = Literal[
    "all",
    "trailing-whitespace",
    "end-of-file-fixer",
    "check-yaml",
    "check-toml",
    "ruff",
    "ruff-format",
    "detect-secrets",
    "pymarkdown",
    "relint",
]


@task(
    help={
        "test": f"Linters to run {LinterType.__args__}",
        "all_files": "Specify to check all files instead of the stage area",
    }
)
def lint(cmd, test="all", all_files=False):
    """Run linters"""
    if "all" in test:
        cmd.run(f"pre-commit run{' --all-files' if all_files else '' }")
    else:
        cmd.run(f"pre-commit run{' --all-files' if all_files else '' } {test}")
