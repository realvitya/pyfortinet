"""Invoke task file"""

import shutil
import sys
from pathlib import Path
from typing import Literal

from invoke import Context, Exit, task


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


def _generate_docs(cmd: Context) -> None:
    """Generate reference pages using the same interpreter as Invoke."""
    if sys.version_info < (3, 11):
        raise Exit("Documentation builds require Python 3.11 or later; library usage supports Python 3.9.")
    cmd.run(f'"{sys.executable}" docs/gen_ref_pages.py')


@task(aliases=["mkdocs"])
def docs(cmd: Context) -> None:
    """Generate API pages and build the documentation with Zensical."""
    _generate_docs(cmd)
    cmd.run("zensical build --strict")


MODULES = Literal["unit", "transport", "all"]


@task(
    help={
        "module": f"Test only on modules from this list: {MODULES.__args__}",
        "verbose": "Print out all test function name",
    }
)
def test(cmd, module: MODULES = "all", verbose=False):
    """Run offline unit and/or loopback transport tests."""
    dirs = {
        "unit": "tests/unit",
        "transport": "tests/transport",
        "all": "tests/unit tests/transport",
    }
    test_target = dirs[module]
    cmd.run(f"uv run pytest {'-vvv' if verbose else ''} {test_target}")


LAB_MODULES = Literal["async", "sync", "objects", "all"]


@task(help={"module": "Lab subtree: async, sync, objects, or all", "baseline": "Enable authorized install tests"})
def lab_test(cmd, module: LAB_MODULES = "all", verbose=False, baseline=False):
    """Run explicitly selected lab tests serially with local lab settings."""
    dirs = {
        "async": "tests/lab/async",
        "sync": "tests/lab/sync",
        "objects": "tests/lab/sync/objects tests/lab/async/objects",
        "all": "tests/lab",
    }
    baseline_option = "--run-baseline-tests" if baseline else ""
    cmd.run(
        f"uv run pytest {'-vvv' if verbose else ''} --lab_config private/lab-config.yml "
        f"{baseline_option} {dirs[module]}"
    )


@task(aliases=["mkdocs-serve"])
def docs_serve(cmd: Context) -> None:
    """Generate API pages and preview the documentation with Zensical."""
    _generate_docs(cmd)
    cmd.run("zensical serve")


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
        cmd.run(f"pre-commit run{' --all-files' if all_files else ''}")
    else:
        cmd.run(f"pre-commit run{' --all-files' if all_files else ''} {test}")
