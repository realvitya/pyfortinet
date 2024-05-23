"""Test of human API"""

import pytest

from pyfortinet import AsyncFMG
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.firewall import Address, AddressGroup, ServiceCustom
from tests.conftest import AsyncTestCase


@pytest.mark.usefixtures("fmg")
@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_firewall_address(self, fmg):
        to_add = fmg.get_obj(Address(name="test-firewall-address", subnet="10.0.0.0/24", allow_routing="disable"))
        # test ADD
        result = to_add.add()
        assert result
        # test CLONE
        result = to_add.clone(name="clone-firewall-address")
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
        # cleanup
        cloned = fmg.get(Address, F(name="clone-firewall-address")).first()
        result = cloned.delete()
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

    def test_firewall_address_group(self, fmg):
        # create members
        member1 = fmg.get_obj(Address(name="test-address1", subnet="10.0.0.1"))
        member2 = fmg.get_obj(Address(name="test-address2", subnet="10.0.0.2"))
        member3 = fmg.get_obj(Address(name="test-address3", subnet="10.0.0.3"))
        member1.add()
        member2.add()
        member3.add()
        # create groups with members
        group1 = fmg.get_obj(AddressGroup(name="test-group1", member=[member1, member2]))
        group2 = fmg.get_obj(AddressGroup(name="test-group2", member=[member1, group1]))
        assert group1.add()
        assert group2.add()
        # add member3 in-memory
        group1.member.append(member3)
        # update FMG
        assert group1.update()
        # reload from FMG
        group1.refresh()
        # check if members still match from FMG loaded object
        assert group1.member == ["test-address1", "test-address2", "test-address3"]
        # deleting objects must follow dependency tree else FMG error out by deleting object used
        group2.delete()
        group1.delete()
        member1.delete()
        member2.delete()

    def test_firewall_custom_service(self, fmg):
        services = fmg.get(ServiceCustom)
        assert services["QUAKE", "name"].name == "QUAKE" and services["QUAKE"].name == "QUAKE"
        with pytest.raises(AttributeError):
            quake = services["QUAKE", "qweqweqwe"]
        assert services


class TestAsynchObjectsOnLab(AsyncTestCase):
    async def test_firewall_address(self, fmg: AsyncFMG):
        to_add = fmg.get_obj(Address(name="test-firewall-address", subnet="10.0.0.0/24", allow_routing="disable"))
        # test ADD
        result = await to_add.add()
        assert result
        # test CLONE
        result = await to_add.clone(name="clone-firewall-address")
        assert result
        # wildcard test
        wildcard = fmg.get_obj(Address(name="test-wildcard", type="wildcard", wildcard="10.0.0.1 255.255.0.255"))
        result = await wildcard.add()
        assert result
        wildcard = (await fmg.get(Address, F(name="test-wildcard"))).first()
        assert wildcard
        await wildcard.delete()
        # test GET
        address = (await fmg.get(Address, F(name__like="test-firewall-addr%"))).first()
        assert address.name == "test-firewall-address"
        address.subnet = "10.0.1.0/24"
        # test UPDATE
        result = await address.update()
        assert result
        address = (await fmg.get(Address, F(name=address.name))).first()
        assert address.subnet == "10.0.1.0/24"
        # test DELETE
        result = await address.delete()
        assert result
        result = await fmg.get(Address, F(name="test-firewall-address"))
        assert result and not result.data  # ensure empty result
        # test SET
        result = await to_add.set()
        assert result
        # cleanup
        cloned = (await fmg.get(Address, F(name="clone-firewall-address"))).first()
        result = await cloned.delete()
        assert result
        result = await to_add.delete()
        assert result
        result = await fmg.get(Address, F(name="test-firewall-address"))
        assert result and not result.data  # ensure empty result

    async def test_firewall_address_mapping(self, fmg: AsyncFMG):
        # create a new object
        server: Address = fmg.get_obj(Address(name="test-server", subnet="10.0.0.1/32"))
        # get first device from FMG
        fw: Device = (await fmg.get(Device)).first()
        # create server object in FMG
        await server.add()
        # create a mapping to server object with the fw device and different IP
        # server.dynamic_mapping = [Address(mapping__scope=[{"name": fw.name, "vdom": "root"}], subnet="2.2.2.2")]
        server.dynamic_mapping = [Address(mapping__scope=fw.get_vdom_scope("root"), subnet="2.2.2.2")]
        # update server object in FMG
        result = await server.update()
        assert result
        # re-load server object from FMG
        server: Address = (await fmg.get(Address, F(name="test-server"))).first()
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

    async def test_firewall_address_group(self, fmg: AsyncFMG):
        # create members
        member1 = fmg.get_obj(Address(name="test-address1", subnet="10.0.0.1"))
        member2 = fmg.get_obj(Address(name="test-address2", subnet="10.0.0.2"))
        member3 = fmg.get_obj(Address(name="test-address3", subnet="10.0.0.3"))
        await member1.add()
        await member2.add()
        await member3.add()
        # create groups with members
        group1 = fmg.get_obj(AddressGroup(name="test-group1", member=[member1, member2]))
        group2 = fmg.get_obj(AddressGroup(name="test-group2", member=[member1, group1]))
        assert await group1.add()
        assert await group2.add()
        # add member3 in-memory
        group1.member.append(member3)
        # update FMG
        assert await group1.update()
        # reload from FMG
        await group1.refresh()
        # check if members still match from FMG loaded object
        assert group1.member == ["test-address1", "test-address2", "test-address3"]
        # deleting objects must follow dependency tree else FMG error out by deleting object used
        await group2.delete()
        await group1.delete()
        await member1.delete()
        await member2.delete()

    async def test_firewall_custom_service(self, fmg: AsyncFMG):
        services = await fmg.get(ServiceCustom)
        assert services["QUAKE", "name"].name == "QUAKE" and services["QUAKE"].name == "QUAKE"
        with pytest.raises(AttributeError):
            quake = services["QUAKE", "qweqweqwe"]
        assert services

    async def test_firewall_custom_service_group(self, fmg: AsyncFMG):
        services = await fmg.get(ServiceCustom)
        assert services
