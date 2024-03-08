"""FMGBase tests"""
import asyncio
from copy import deepcopy

import pytest
import pytest_asyncio
from aiohttp import ClientConnectorError
from pydantic import SecretStr, ValidationError

from pyfortinet import AsyncFMGBase, FMG, fmg
from pyfortinet import exceptions as fe
from pyfortinet.settings import FMGSettings

need_lab = pytest.mark.skipif(not pytest.lab_config, reason=f"Lab config {pytest.lab_config_file} does not exist!")


class TestAsyncFMGSettings:
    """AsyncFMGSettings test module"""

    config = {
        "base_url": "https://somehost",
        "verify": False,
        "username": "myuser",
        "password": "verysecret",
        "adom": "root",
    }

    def test_fmg_settings(self):
        settings = FMGSettings(**self.config)
        assert "jsonrpc" in settings.base_url.path

    def test_fmg_settings_bad_url(self):
        config = deepcopy(self.config)
        config["base_url"] = "somehost"
        with pytest.raises(ValidationError, match="Input should be a valid URL"):
            FMGSettings(**config)

    def test_fmg_object_creation_by_object(self):
        config = deepcopy(self.config)
        settings = FMGSettings(**config)
        AsyncFMGBase(settings)

    def test_fmg_object_creation_by_kwargs(self):
        config = deepcopy(self.config)
        AsyncFMGBase(**config)

    async def test_fmg_need_to_open_first(self):
        config = deepcopy(self.config)
        with pytest.raises(fe.FMGTokenException, match="Open connection first!"):
            settings = FMGSettings(**config)
            conn = AsyncFMGBase(settings)
            await conn.get_version()


@need_lab
class TestLab:
    """Lab tests"""

    config = pytest.lab_config.get("fmg")  # configured in conftest.py

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_fmg_lab_connect(self, prepare_lab):
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            ver = await conn.get_version()
        assert "-build" in ver

    @pytest.mark.asyncio
    async def test_fmg_lab_connect_wrong_creds(self, prepare_lab):
        config = deepcopy(self.config)
        config["password"] = "badpassword"  # pragma: allowlist secret
        settings = FMGSettings(**config)
        conn = AsyncFMGBase(settings)
        with pytest.raises(fe.FMGTokenException, match="Login failed, wrong credentials!"):
            await conn.open()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    @pytest.mark.asyncio
    async def test_fmg_lab_connection_error(self):
        config = deepcopy(self.config)
        config["base_url"] = "https://127.0.0.1"
        settings = FMGSettings(**config)
        conn = AsyncFMGBase(settings)
        with pytest.raises(ClientConnectorError):
            await conn.open()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    @pytest.mark.asyncio
    async def test_fmg_lab_expired_session(self, prepare_lab):
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
            await conn.get_version()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    @pytest.mark.asyncio
    async def test_fmg_lab_expired_session_and_wrong_creds(self, prepare_lab):
        """Simulate expired token and changed credentials"""
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
            conn._settings.password = SecretStr("bad_password")
            with pytest.raises(fe.FMGTokenException, match="wrong credentials"):
                await conn.get_version()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    @pytest.mark.asyncio
    async def test_fmg_lab_fail_logout_with_expired_token(self, prepare_lab, caplog):
        """Simulate expired token by logout"""
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
        assert "Logout failed" in caplog.text

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    @pytest.mark.asyncio
    async def test_fmg_lab_fail_logout_with_disconnect(self, prepare_lab, caplog):
        """Simulate disconnection by logout"""
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            conn._settings.base_url = "https://127.0.0.1/jsonrpc"

        assert "Logout failed" in caplog.text


@need_lab
class TestObjectsOnLab:
    async_fmg_base = None

    @pytest.fixture(scope="session")
    def event_loop(self):
        loop = asyncio.get_event_loop()
        yield loop
        loop.close()

    @pytest.fixture(autouse=True, scope='class')
    async def _async_fmg_base_fixture(self):
        # assuming AsyncFMGBase is defined somewhere and we create an instance of it
        TestObjectsOnLab.async_fmg_base = AsyncFMGBase(FMGSettings(**pytest.lab_config.get("fmg")))

        # Call the async setup method
        await TestObjectsOnLab.async_fmg_base.open()

        yield TestObjectsOnLab.async_fmg_base

        # Call the async teardown method after the test case
        await TestObjectsOnLab.async_fmg_base.close(discard_changes=True)

    async def test_address_add_dict(self):
        scope = "global" if self.async_fmg_base.adom == "global" else f"adom/{self.async_fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "data": {
                "name": "test-address",
                "subnet": "10.0.0.1/32",
            },
        }
        result = await self.async_fmg_base.add(address_request)
        assert result.success

    async def test_address_del_dict(self):
        scope = "global" if self.async_fmg_base.adom == "global" else f"adom/{self.async_fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
        }
        result = await self.async_fmg_base.delete(address_request)
        assert result.success
