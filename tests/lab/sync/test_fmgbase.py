"""FMGBase tests"""

import pytest

from pyfortinet import FMGBase
from pyfortinet.settings import FMGSettings

need_lab = pytest.mark.skipif(not pytest.lab_config, reason=f"Lab config {pytest.lab_config_file} does not exist!")


@need_lab
@pytest.mark.filterwarnings("ignore:Unverified")
class TestLab:
    """Lab tests"""

    config = pytest.lab_config.get("fmg")  # configured in conftest.py

    def test_fmg_lab_connect(self):
        settings = FMGSettings(**self.config)
        with FMGBase(settings) as conn:
            ver = conn.get_version()
        assert "-build" in ver


@pytest.mark.usefixtures("fmg_base")
@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def _address_add_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "data": {
                "name": "test-address",
                "subnet": "10.0.0.1/32",
            },
        }
        result = fmg_base.add(address_request)
        assert result.success

    def _address_add_dict_bad_subnet(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "data": {
                "name": "test-address",
                "subnet": "badvalue",
            },
        }
        fmg_base.raise_on_error = False
        result = fmg_base.add(address_request)
        assert not result.success and "data is invalid" in result.data[0]["error"]
        fmg_base.raise_on_error = True

    def _address_multiple_add_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = [
            {
                "url": f"/pm/config/{scope}/obj/firewall/address",
                "data": {
                    "name": "test-address10",
                    "subnet": "10.0.0.10/32",
                },
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address",
                "data": {
                    "name": "test-address11",
                    "subnet": "10.0.0.11/32",
                },
            },
        ]
        result = fmg_base.add(address_request)
        assert result.success
        # iterate over the result
        for res in result:
            assert "test-address" in res.get("data").get("name")
        # using correct master_key gives back that specific result dict
        res = result["test-address10", "name"]
        assert res["data"]["name"] == "test-address10"
        # wrong master_key gives None
        assert result["test-address10", "qweqwe"] is None
        # master_key would be mandatory by dict data
        with pytest.raises(AttributeError, match="Invalid key"):
            res = result["test-address10"]
        # test sequence get
        res = result[0]
        assert res["data"]["name"] == "test-address10"

    def _address_update_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "subnet": "10.0.0.2/32",
            },
        }
        result = fmg_base.update(address_request)
        assert result.success

    def _address_multiple_update_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = [
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address10",
                "data": {
                    "subnet": "10.0.0.100/32",
                },
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address11",
                "data": {
                    "subnet": "10.0.0.111/32",
                },
            },
        ]
        result = fmg_base.update(address_request)
        assert result.success

    def _address_get_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "filter": [["name", "==", "test-address"]],
        }
        result = fmg_base.get(address_request)
        assert result.success and result.data[0]["data"][0].get("name") == "test-address"

    def _address_del_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
        }
        result = fmg_base.delete(address_request)
        assert result.success

    def _address_multiple_del_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = [
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address10",
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address11",
            },
        ]
        result = fmg_base.delete(address_request)
        assert result.success

    def _address_set_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "subnet": "10.0.0.2/32",
            },
        }
        result = fmg_base.set(address_request)
        assert result.success

    def _address_multiple_set_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = [
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address10",
                "data": {
                    "subnet": "10.0.0.10/32",
                },
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address11",
                "data": {
                    "subnet": "10.0.0.11/32",
                },
            },
        ]
        result = fmg_base.set(address_request)
        assert result.success

    def _address_clone_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",  # source object
            "data": {
                "name": "clone-address",  # destination object
            },
        }
        result = fmg_base.clone(address_request)
        assert result.success

    def _address_multiple_clone_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = [
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address10",  # source object
                "data": {
                    "name": "clone-address10",  # destination object
                },
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address11",  # source object
                "data": {
                    "name": "clone-address11",  # destination object
                },
            },
        ]
        result = fmg_base.clone(address_request)
        assert result.success

    def _address_cleanup(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = [
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address10",
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/test-address11",
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/clone-address",
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/clone-address10",
            },
            {
                "url": f"/pm/config/{scope}/obj/firewall/address/clone-address11",
            },
        ]
        result = fmg_base.delete(address_request)
        assert result.success

    def test_address_lifecycle(self, fmg_base, base_lab):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        for name in [
            "test-address",
            "test-address10",
            "test-address11",
            "clone-address",
            "clone-address10",
            "clone-address11",
        ]:
            base_lab.reserve(f"/pm/config/{scope}/obj/firewall/address/{name}")
        self._address_add_dict(fmg_base)
        self._address_add_dict_bad_subnet(fmg_base)
        self._address_multiple_add_dict(fmg_base)
        self._address_update_dict(fmg_base)
        self._address_multiple_update_dict(fmg_base)
        self._address_get_dict(fmg_base)
        self._address_del_dict(fmg_base)
        self._address_multiple_del_dict(fmg_base)
        self._address_set_dict(fmg_base)
        self._address_multiple_set_dict(fmg_base)
        self._address_clone_dict(fmg_base)
        self._address_multiple_clone_dict(fmg_base)
        self._address_cleanup(fmg_base)
