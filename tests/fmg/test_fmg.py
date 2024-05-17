"""Test of human API"""

import pytest
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.firewall import Address


@pytest.mark.usefixtures("fmg")
class TestObjectsOnLab:
    def test_get_adom_list(self, fmg):
        result = fmg.get_adom_list(F(name__like="root"))  # root filter
        assert result == ["root"]

    def test_get_adom_list_with_or_filters(self, fmg):
        result = fmg.get_adom_list(F(name__like="root") | F(name__like="rootp"))
        assert result == ["root", "rootp"]

    def test_get_adom_list_with_three_filters(self, fmg):
        result = fmg.get_adom_list(F(name__like="root") | (F(name__like="rootp") | F(name="others")))
        assert result == ["others", "root", "rootp"]

    def test_get_adom_list_with_three_filters2(self, fmg):
        result = fmg.get_adom_list(F(name__like="root") + (F(name__like="rootp") + F(name="others")))
        assert result == ["others", "root", "rootp"]

    def test_get_adom_list_with_complex_filter(self, fmg):
        result = fmg.get_adom_list((F(name__like="root") + (F(name__like="rootp") + F(name="others")) & F(state=1)))
        assert result == ["others", "root", "rootp"]

    def test_multi_obj(self, fmg):
        addr1 = fmg.get_obj(Address(name="test-addr1", subnet="10.0.0.1/32"))
        addr2 = fmg.get_obj(Address(name="test-addr2", subnet="10.0.0.2/32"))
        result = fmg.add([addr1, addr2])
        assert result
        addr1.subnet = "10.0.0.11/32"
        addr2.subnet = "10.0.0.12/32"
        result = fmg.update([addr1, addr2])
        assert result
        addr1.subnet = "10.0.0.11/32"
        addr2.subnet = "10.0.0.12/32"
        result = fmg.set([addr1, addr2])
        assert result
        result = fmg.delete([addr1, addr2])
        assert result
        # ensure object is deleted
        result = fmg.get(Address, F(name="test-addr1")).first()
        assert result is None
