"""Pytest configuration and per-test lab connections."""

from pathlib import Path

import pytest
import pytest_asyncio
from ruamel.yaml import YAML

from pyfortinet import FMG, AsyncFMG, AsyncFMGBase, FMGBase, FMGSettings
from pyfortinet.fmg_api.dvmdb import Device
from tests.lab_resources import AsyncLabResources, LabResources


def pytest_addoption(parser):
    parser.addoption("--lab_config", action="store", default="lab-config.yml")
    parser.addoption(
        "--run-baseline-tests", action="store_true", help="Run install tests requiring an authorized snapshot restore"
    )


def pytest_configure(config):
    pytest.lab_config_file = Path(config.getoption("--lab_config"))
    pytest.lab_config = {}
    if pytest.lab_config_file.is_file():
        pytest.lab_config = YAML(typ="safe", pure=True).load(pytest.lab_config_file) or {}
    config.addinivalue_line("markers", "requires_baseline: installs configuration; requires snapshot-based restoration")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-baseline-tests"):
        skip = pytest.mark.skip(reason="Requires an authorized baseline restore and --run-baseline-tests")
        for item in items:
            if item.get_closest_marker("requires_baseline"):
                item.add_marker(skip)


def lab_settings() -> FMGSettings:
    """Never attempt a lab connection when no credentials were supplied."""
    if not pytest.lab_config.get("fmg"):
        pytest.skip(f"Lab config {pytest.lab_config_file} has no fmg settings")
    return FMGSettings(**pytest.lab_config["fmg"])


@pytest.fixture
def fmg_base():
    client = FMGBase(lab_settings())
    try:
        client.open()
        yield client
    finally:
        client.close(discard_changes=True)


@pytest.fixture
def fmg():
    client = FMG(lab_settings())
    try:
        client.open()
        yield client
    finally:
        client.close(discard_changes=True)


@pytest.fixture
def lab(fmg):
    resources = LabResources(fmg)
    try:
        yield resources
    finally:
        resources.cleanup()


@pytest.fixture
def base_lab(fmg_base):
    resources = LabResources(fmg_base)
    try:
        yield resources
    finally:
        resources.cleanup()


@pytest.fixture
def lab_device(fmg):
    """Use the policy's named device rather than whichever device happens to be first."""
    device = fmg.get(Device(name="FG01")).first()
    assert device is not None, "Expected authorized device FG01 in the configured ADOM"
    return device


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore:Unverified")
class AsyncTestCase:
    """Request only the async connection needed by this individual test."""

    @pytest_asyncio.fixture
    async def fmg_base(self):
        client = AsyncFMGBase(lab_settings())
        try:
            await client.open()
            yield client
        finally:
            await client.close(discard_changes=True)

    @pytest_asyncio.fixture
    async def fmg(self):
        client = AsyncFMG(lab_settings())
        try:
            await client.open()
            yield client
        finally:
            await client.close(discard_changes=True)

    @pytest_asyncio.fixture
    async def lab(self, fmg):
        resources = AsyncLabResources(fmg)
        try:
            yield resources
        finally:
            await resources.cleanup()

    @pytest_asyncio.fixture
    async def base_lab(self, fmg_base):
        resources = AsyncLabResources(fmg_base)
        try:
            yield resources
        finally:
            await resources.cleanup()

    @pytest_asyncio.fixture
    async def lab_device(self, fmg):
        device = (await fmg.get(Device(name="FG01"))).first()
        assert device is not None, "Expected authorized device FG01 in the configured ADOM"
        return device
