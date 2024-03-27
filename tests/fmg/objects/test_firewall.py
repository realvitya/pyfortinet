"""Test of human API"""

import pytest
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.firewall import Address


@pytest.mark.usefixtures("fmg")
class TestObjectsOnLab:
    def test_firewall_address(self, fmg):
        to_add = fmg.get_obj(Address(name="test-firewall-address", subnet="10.0.0.0/24", allow_routing="disable"))
        # test ADD
        result = to_add.add()
        assert result
        # wildcard test
        wildcard = fmg.get_obj(Address(name="test-wildcard", type="wildcard", wildcard="10.0.0.1 255.255.0.255"))
        result = wildcard.add()
        assert result
        wildcard = fmg.get(Address, F(name="test-wildcard")).first()
        assert wildcard
        wildcard.delete()
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

    def test_firewall_address_mapping(self, fmg):
        # create a new object
        server: Address = fmg.get_obj(Address(name="test-server", subnet="10.0.0.1/32"))
        # get first device from FMG
        fw: Device = fmg.get(Device).first()
        # create server object in FMG
        server.add()
        # create a mapping to server object with the fw device and different IP
        # server.dynamic_mapping = [Address(mapping__scope=[{"name": fw.name, "vdom": "root"}], subnet="2.2.2.2")]
        server.dynamic_mapping = [Address(mapping__scope=fw.get_vdom_scope("root"), subnet="2.2.2.2")]
        # update server object in FMG
        result = server.update()
        assert result
        # re-load server object from FMG
        server: Address = fmg.get(Address, F(name="test-server")).first()
        # check if we have our mapping
        assert any(address.subnet == "2.2.2.2/32" for address in server.dynamic_mapping)
        #
        # commented out as I referenced a 2nd FW (FG02) which I do not expect in the lab
        #
        # # create new mapping with FG02 device (I created a model device for testing)
        # server.dynamic_mapping.append(Address(mapping__scope=[{"name": "FG02", "vdom": "root"}], subnet="3.3.3.3"))
        # result = server.update()
        # assert result
        # server = fmg.get(Address, F(name="test-server")).first()
        # assert server
        # # delete mapping (simply removing from the list works. Could be more sophisticated, but good for example)
        # del server.dynamic_mapping[1]
        # server.update()
        # server = fmg.get(Address, F(name="test-server")).first()
        # # check if we still have the first mapping
        # assert any(address.subnet == "2.2.2.2/32" for address in server.dynamic_mapping)
        # # check if we really deleted the second mapping
        # assert not any(address.subnet == "3.3.3.3/32" for address in server.dynamic_mapping)
