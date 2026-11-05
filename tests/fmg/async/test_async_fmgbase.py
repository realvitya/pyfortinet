"""FMGBase tests"""

from copy import deepcopy

import pytest
from pydantic import ValidationError

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
@pytest.mark.filterwarnings("ignore:Unverified")
class TestLab(AsyncTestCase):
    """Lab tests"""

    config = pytest.lab_config.get("fmg")  # configured in conftest.py

    async def test_fmg_lab_connect(self):
        settings = FMGSettings(**self.config)
        async with AsyncFMGBase(settings) as conn:
            ver = await conn.get_version()
        assert "-build" in ver


class TestObjectsOnLab(AsyncTestCase):
    async def _address_add_dict(self, fmg_base):
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

    async def _address_add_dict_bad_subnet(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "data": {
                "name": "test-address",
                "subnet": "badvalue",
            },
        }
        fmg_base.raise_on_error = False
        result = await fmg_base.add(address_request)
        assert not result.success and "data is invalid" in result.data[0]["error"]
        fmg_base.raise_on_error = True

    async def _address_update_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "subnet": "10.0.0.2/32",
            },
        }
        result = await fmg_base.update(address_request)
        assert result.success

    async def _address_get_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "filter": [["name", "==", "test-address"]],
        }
        result = await fmg_base.get(address_request)
        assert result.success and result.data[0]["data"][0].get("name") == "test-address"

    async def _address_del_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
        }
        result = await fmg_base.delete(address_request)
        assert result.success

    async def _address_set_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "subnet": "10.0.0.2/32",
            },
        }
        result = await fmg_base.set(address_request)
        assert result.success

    async def _address_cleanup(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
        }
        result = await fmg_base.delete(address_request)
        assert result.success

    async def test_address_lifecycle(self, fmg_base, base_lab):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        for name in [
            "test-address",
            "test-address10",
            "test-address11",
            "clone-address",
            "clone-address10",
            "clone-address11",
        ]:
            await base_lab.reserve(f"/pm/config/{scope}/obj/firewall/address/{name}")
        await self._address_add_dict(fmg_base)
        await self._address_add_dict_bad_subnet(fmg_base)
        await self._address_update_dict(fmg_base)
        await self._address_get_dict(fmg_base)
        await self._address_del_dict(fmg_base)
        await self._address_set_dict(fmg_base)
        await self._address_cleanup(fmg_base)
