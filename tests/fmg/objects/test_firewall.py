"""Test of human API"""

import pytest
from pyfortinet import FMG, FMGSettings
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.firewall import Address


@pytest.mark.usefixtures("fmg")
class TestObjectsOnLab:
    def test_firewall_address(self, fmg):
        to_add = fmg.get_obj(Address, name="test-firewall-address", subnet="10.0.0.0/24", allow_routing="disable")
        # test ADD
        result = to_add.add()
        assert result
        # test GET
        address = fmg.get(Address, F(name__like="test-firewall-addr%")).first()
        assert address.name == "test-firewall-address"
        address.subnet = "10.0.1.0/24"
        # test UPDATE
        result = address.update()
        assert result
        address = fmg.get(Address, F(name=address.name)).first()
        assert address.subnet == "10.0.1.0/24"
        # test DELETE
        result = address.delete()
        assert result
        result = fmg.get(Address, F(name="test-firewall-address"))
        assert result and not result.data  # ensure empty result
        # test SET
        result = to_add.set()
        assert result
        result = to_add.delete()
        assert result
        result = fmg.get(Address, F(name="test-firewall-address"))
        assert result and not result.data  # ensure empty result

    # def test_firewall_address_mapping(self, fmg):
    #     server = fmg.get_obj(Address, name="test-server", subnet="10.0.0.1/32")
    #     FG01 = fmg.get(Device, F(name="FG01")).first()
    #     assert True
