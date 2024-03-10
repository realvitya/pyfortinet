"""FMGBase tests"""
from copy import deepcopy

import pytest
from aiohttp import ClientConnectorError
from pydantic import SecretStr, ValidationError

from pyfortinet import AsyncFMGBase
from pyfortinet import exceptions as fe
from pyfortinet.settings import FMGSettings
from tests.conftest import AsyncTestCase

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
@pytest.mark.usefixtures("prepare_lab")
class TestLab:
    """Lab tests"""

    config = pytest.lab_config.get("fmg")  # configured in conftest.py

    @pytest.mark.dependency()
    async def test_fmg_lab_connect(self):
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            ver = await conn.get_version()
        assert "-build" in ver

    async def test_fmg_lab_connect_wrong_creds(self):
        config = deepcopy(self.config)
        config["password"] = "badpassword"  # pragma: allowlist secret
        settings = FMGSettings(**config)
        conn = AsyncFMGBase(settings)
        with pytest.raises(fe.FMGTokenException, match="Login failed, wrong credentials!"):
            await conn.open()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    async def test_fmg_lab_connection_error(self):
        config = deepcopy(self.config)
        config["base_url"] = "https://127.0.0.1"
        settings = FMGSettings(**config)
        conn = AsyncFMGBase(settings)
        with pytest.raises(ClientConnectorError):
            await conn.open()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    async def test_fmg_lab_expired_session(self):
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
            await conn.get_version()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    async def test_fmg_lab_expired_session_and_wrong_creds(self, prepare_lab):
        """Simulate expired token and changed credentials"""
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
            conn._settings.password = SecretStr("bad_password")
            with pytest.raises(fe.FMGTokenException, match="wrong credentials"):
                await conn.get_version()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    async def test_fmg_lab_fail_logout_with_expired_token(self, prepare_lab, caplog):
        """Simulate expired token by logout"""
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
        assert "Logout failed" in caplog.text

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    async def test_fmg_lab_fail_logout_with_disconnect(self, prepare_lab, caplog):
        """Simulate disconnection by logout"""
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            conn._settings.base_url = "https://127.0.0.1/jsonrpc"

        assert "Logout failed" in caplog.text


class TestObjectsOnLab(AsyncTestCase):
    async def test_address_add_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "data": {
                "name": "test-address",
                "subnet": "10.0.0.1/32",
            },
        }
        result = await fmg_base.add(address_request)
        assert result.success

    async def test_address_update_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "subnet": "10.0.0.2/32",
            },
        }
        result = await fmg_base.update(address_request)
        assert result.success

    async def test_address_get_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "filter": [["name", "==", "test-address"]],
        }
        result = await fmg_base.get(address_request)
        assert result.success and result.data["data"][0].get("name") == "test-address"

    async def test_address_del_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
        }
        result = await fmg_base.delete(address_request)
        assert result.success

    async def test_address_set_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "subnet": "10.0.0.2/32",
            },
        }
        result = await fmg_base.set(address_request)
        assert result.success

    async def test_address_cleanup(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
        }
        result = await fmg_base.delete(address_request)
        assert result.success
