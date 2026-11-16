"""Function-scoped live connections and owned lab resources."""

import pytest
import pytest_asyncio

from pyfortinet import FMG, AsyncFMG, AsyncFMGBase, FMGBase, FMGSettings
from pyfortinet.fmg_api.dvmdb import Device
from tests.lab.resources import AsyncLabResources, LabResources


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
