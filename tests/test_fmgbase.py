"""FMGBase tests"""
from copy import deepcopy

import pytest
from pydantic import SecretStr, ValidationError
from requests.exceptions import ConnectionError

from pyfortinet import FMGBase
from pyfortinet import exceptions as fe
from pyfortinet.settings import FMGSettings

need_lab = pytest.mark.skipif(not pytest.lab_config, reason=f"Lab config {pytest.lab_config_file} does not exist!")


class TestFMGSettings:
    """FMGSettings test module"""

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
        FMGBase(settings)

    def test_fmg_object_creation_by_kwargs(self):
        config = deepcopy(self.config)
        FMGBase(**config)

    def test_fmg_need_to_open_first(self):
        config = deepcopy(self.config)
        with pytest.raises(fe.FMGTokenException, match="Open connection first!"):
            settings = FMGSettings(**config)
            conn = FMGBase(settings)
            conn.get_version()


@need_lab
class TestLab:
    """Lab tests"""

    config = pytest.lab_config.get("fmg")  # configured in conftest.py

    @pytest.mark.dependency()
    def test_fmg_lab_connect(self, prepare_lab):
        settings = FMGSettings(**self.config)
        with FMGBase(settings) as conn:
            ver = conn.get_version()
        assert "-build" in ver

    def test_fmg_lab_connect_wrong_creds(self, prepare_lab):
        config = deepcopy(self.config)
        config["password"] = "badpassword"  # pragma: allowlist secret
        settings = FMGSettings(**config)
        conn = FMGBase(settings)
        with pytest.raises(fe.FMGTokenException, match="Login failed, wrong credentials!"):
            conn.open()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    def test_fmg_lab_connection_error(self):
        config = deepcopy(self.config)
        config["base_url"] = "https://127.0.0.1"
        settings = FMGSettings(**config)
        conn = FMGBase(settings)
        with pytest.raises(ConnectionError):
            conn.open()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    def test_fmg_lab_expired_session(self, prepare_lab):
        settings = FMGSettings(**self.config)
        with FMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
            conn.get_version()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    def test_fmg_lab_expired_session_and_wrong_creds(self, prepare_lab):
        """Simulate expired token and changed credentials"""
        settings = FMGSettings(**self.config)
        with FMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
            conn._settings.password = SecretStr("bad_password")
            with pytest.raises(fe.FMGTokenException, match="wrong credentials"):
                conn.get_version()

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    def test_fmg_lab_fail_logout_with_expired_token(self, prepare_lab, caplog):
        """Simulate expired token by logout"""
        settings = FMGSettings(**self.config)
        with FMGBase(settings) as conn:
            conn._token = SecretStr("bad_token")
        assert "Logout failed" in caplog.text

    @pytest.mark.dependency(depends=["TestLab::test_fmg_lab_connect"])
    def test_fmg_lab_fail_logout_with_disconnect(self, prepare_lab, caplog):
        """Simulate disconnection by logout"""
        settings = FMGSettings(**self.config)
        with FMGBase(settings) as conn:
            conn._settings.base_url = "https://127.0.0.1/jsonrpc"

        assert "Logout failed" in caplog.text


@pytest.mark.usefixtures("fmg_base")
class TestObjectsOnLab:
    def test_address_add_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "name": "test-address",
                "subnet": "10.0.0.1/32",
            },
        }
        result = fmg_base.add(address_request)
        assert result.success

    def test_address_update_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "subnet": "10.0.0.2/32",
            },
        }
        result = fmg_base.update(address_request)
        assert result.success

    def test_address_get_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address",
            "filter": [["name", "==", "test-address"]],
        }
        result = fmg_base.get(address_request)
        assert result.success and result.data["data"][0].get("name") == "test-address"

    def test_address_del_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
        }
        result = fmg_base.delete(address_request)
        assert result.success

    def test_address_set_dict(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
            "data": {
                "subnet": "10.0.0.2/32",
            },
        }
        result = fmg_base.set(address_request)
        assert result.success

    def test_address_cleanup(self, fmg_base):
        scope = "global" if fmg_base.adom == "global" else f"adom/{fmg_base.adom}"
        address_request = {
            "url": f"/pm/config/{scope}/obj/firewall/address/test-address",
        }
        result = fmg_base.delete(address_request)
        assert result.success
