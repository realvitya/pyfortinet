"""Test of human API"""
import pytest
from pyfortinet import FMG, FMGSettings
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmbd import Device
from pyfortinet.fmg_api.firewall import Address

need_lab = pytest.mark.skipif(not pytest.lab_config, reason=f"Lab config {pytest.lab_config_file} does not exist!")


@need_lab
class TestObjectsOnLab:
    fmg = FMG(FMGSettings(**pytest.lab_config.get("fmg"))).open()
    fmg_connected = pytest.mark.skipif(
        not fmg._token, reason=f"FMG {pytest.lab_config.get('fmg', {}).get('base_url')} is not connected!"
    )

    @fmg_connected
    def test_get_adom_list(self):
        result = self.fmg.get_adom_list(F(name__like="root"))  # root filter
        assert result == ["root"]

    @fmg_connected
    def test_get_adom_list_with_or_filters(self):
        result = self.fmg.get_adom_list(F(name__like="root") | F(name__like="rootp"))
        assert result == ["root", "rootp"]

    @fmg_connected
    def test_get_adom_list_with_three_filters(self):
        result = self.fmg.get_adom_list(F(name__like="root") | (F(name__like="rootp") | F(name="others")))
        assert result == ["others", "root", "rootp"]

    @fmg_connected
    def test_get_adom_list_with_three_filters2(self):
        result = self.fmg.get_adom_list(F(name__like="root") + (F(name__like="rootp") + F(name="others")))
        assert result == ["others", "root", "rootp"]

    @fmg_connected
    def test_get_adom_list_with_complex_filter(self):
        result = self.fmg.get_adom_list(
            (F(name__like="root") + (F(name__like="rootp") + F(name="others")) & F(state=1))
        )
        assert result == ["others", "root", "rootp"]

    @fmg_connected
    def test_get_devices(self):
        result = self.fmg.get(Device, F(name__like="TEST%"))
        assert result

    @fmg_connected
    def test_firewall_address(self):
        to_add = Address(name="test-firewall-address", subnet="10.0.0.0/24")
        result = self.fmg.add(to_add)
        assert result
        address = self.fmg.get(Address, F(name__like="test-firewall-addr%")).first()
        assert address.name == "test-firewall-address"
        result = self.fmg.delete(address)
        assert result.success is True
        result = self.fmg.get(Address, F(name="test-firewall-address"))
        assert not result.data  # empty result

    @fmg_connected
    def test_close_fmg(self):
        self.fmg.close(discard_changes=True)
