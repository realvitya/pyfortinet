"""Pytest setup"""

import asyncio
import time
from pathlib import Path

import pytest
import requests
from ruamel.yaml import YAML

from pyfortinet import FMG, FMGSettings, FMGBase, AsyncFMGBase, AsyncFMG
from pyfortinet.exceptions import FMGConfigurationException


def pytest_addoption(parser):
    """Pytest options"""
    parser.addoption("--lab_config", action="store", default="lab-config.yml")


def pytest_configure(config):
    """Pytest configuration"""
    pytest.lab_config_file = Path(config.getoption("--lab_config"))
    pytest.lab_config = {}
    if pytest.lab_config_file.is_file():
        yaml = YAML(typ="safe", pure=True)
        lab_config = yaml.load(pytest.lab_config_file)
        pytest.lab_config = lab_config


@pytest.fixture(scope="class")
def fmg_base(request):
    # Create FMGBase object
    try:
        fmg = FMGBase(FMGSettings(**pytest.lab_config.get("fmg")))
    except AttributeError as err:
        raise FMGConfigurationException("FMG settings are missing") from err

    # Create connection to FMG
    fmg.open()

    # Give FMG object to test object
    yield fmg

    # Logout and close connection to FMG
    fmg.close(discard_changes=True)


@pytest.fixture(scope="class")
def fmg(request):
    # Create FMG object
    try:
        fmg = FMG(FMGSettings(**pytest.lab_config.get("fmg")))
    except AttributeError as err:
        raise FMGConfigurationException("FMG settings are missing") from err

    # Create connection to FMG
    fmg.open()

    # Give FMG object to test object
    yield fmg

    # Logout and close connection to FMG
    fmg.close(discard_changes=True)


@pytest.mark.asyncio(scope="class")
class AsyncTestCase:
    """Base class for async test cases."""

    # @pytest.fixture(scope="session")
    # def event_loop(self):
    #     """Override default event loop
    #
    #     This fixture overrides event_loop for the class and allows to run everything in a single loop. We get context
    #     manager errors otherwise.
    #     """
    #     # give some time for previous test to correctly logout and clean up
    #     time.sleep(2)
    #     loop = asyncio.get_event_loop()
    #     yield loop
    #     loop.close()

    @pytest.fixture(autouse=True, scope="class")
    async def fmg_base(self):
        """Create and use a single FMG instance during all class tests.

        In order to use this fixture, you need to inherit this class and specify ``fmg`` as argument for each test
        method.

        Examples:
            class TestAsyncStuff(AsyncTestCase):
                async def test_something(self, fmg_base):
                    assert fmg_base.adom
                    ...
        """
        # Create AsyncFMG object
        try:
            fmg_base = AsyncFMGBase(FMGSettings(**pytest.lab_config.get("fmg")))
        except AttributeError as err:
            raise FMGConfigurationException("FMG settings are missing") from err
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

        # Create connection to FMG
        await fmg_base.open()

        # Give FMG object to test object
        yield fmg_base

        # Logout and close connection to FMG
        await fmg_base.close(discard_changes=True)

    @pytest.fixture(autouse=True, scope="class")
    async def fmg(self):
        """Create and use a single FMG instance during all class tests.

        In order to use this fixture, you need to inherit this class and specify ``fmg`` as argument for each test
        method.

        Examples:
            class TestAsyncStuff(AsyncTestCase):
                async def test_something(self, fmg):
                    assert fmg.adom
                    ...
        """
        # Create AsyncFMG object
        try:
            fmg = AsyncFMG(FMGSettings(**pytest.lab_config.get("fmg")))
        except AttributeError as err:
            raise FMGConfigurationException("FMG settings are missing") from err
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

        # Create connection to FMG
        await fmg.open()

        # Give FMG object to test object
        yield fmg

        # Logout and close connection to FMG
        await fmg.close(discard_changes=True)
