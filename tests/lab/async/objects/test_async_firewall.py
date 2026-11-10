"""Independent firewall CRUD tests with per-test resource ownership."""

import pytest

from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.firewall import Address, AddressGroup, PortRange, ServiceCustom, ServiceGroup
from tests.lab.fixtures import AsyncTestCase


class TestObjectsOnLab(AsyncTestCase):
    async def test_firewall_address(self, fmg, lab):
        address = await lab.object(Address, "addr", subnet="10.0.0.0/24", allow_routing="disable")
        clone = await lab.object(Address, "clone")
        assert await address.add()
        assert await address.clone(name=clone.name)
        wildcard = await lab.object(Address, "wild", type="wildcard", wildcard="10.0.0.1 255.255.0.255")
        assert await wildcard.add()
        assert (await fmg.get(Address, F(name=wildcard.name))).first()
        assert await wildcard.delete()
        loaded = (await fmg.get(Address, F(name=address.name))).first()
        assert loaded.name == address.name
        loaded.subnet = "10.0.1.0/24"
        assert await loaded.update()
        await loaded.refresh()
        assert loaded.subnet == "10.0.1.0/24"
        assert await loaded.delete()
        assert (await fmg.get(Address, F(name=address.name))).first() is None
        assert await address.set()
        assert await address.delete()
        assert (await fmg.get(Address, F(name=address.name))).first() is None

    async def test_firewall_address_mapping(self, fmg, lab, lab_device):
        server = await lab.object(Address, "server", subnet="10.0.0.1/32")
        assert await server.add()
        server.dynamic_mapping = [Address(mapping__scope=lab_device.get_vdom_scope("root"), subnet="2.2.2.2")]
        assert await server.update()
        await server.refresh()
        assert any(mapping.subnet == "2.2.2.2/32" for mapping in server.dynamic_mapping)

    async def test_firewall_address_group(self, fmg, lab):
        member1 = await lab.object(Address, "addr1", subnet="10.0.0.1")
        member2 = await lab.object(Address, "addr2", subnet="10.0.0.2")
        member3 = await lab.object(Address, "addr3", subnet="10.0.0.3")
        assert await member1.add()
        assert await member2.add()
        assert await member3.add()
        group1 = await lab.object(AddressGroup, "grp1", member=[member1, member2])
        assert await group1.add()
        group2 = await lab.object(AddressGroup, "grp2", member=[member1, group1])
        assert await group2.add()
        group1.member.append(member3)
        assert await group1.update()
        await group1.refresh()
        assert group1.member == [member1.name, member2.name, member3.name]
        found = (await fmg.get(AddressGroup, F(name=group1.name) & F(member__contain=member1.name))).first()
        assert found.name == group1.name
        found = (
            await fmg.get(
                AddressGroup, F(name=group2.name) & F(member__contain=member1.name) & F(member__contain=group1.name)
            )
        ).first()
        assert found.name == group2.name

    async def test_firewall_custom_service(self, fmg, lab):
        services = await fmg.get(ServiceCustom)
        assert services["QUAKE", "name"].name == "QUAKE" and services["QUAKE"].name == "QUAKE"
        with pytest.raises(AttributeError, match="invalid-key"):
            services["QUAKE", "invalid-key"]
        for ports, expected in [
            (PortRange(destination_end="6666"), ["6666"]),
            ("6666", ["6666"]),
            (["6666", "7777:1-1024"], ["6666", "7777:1-1024"]),
        ]:
            service = await lab.object(ServiceCustom, "srv", tcp_portrange=ports)
            assert service.model_dump(by_alias=True)["tcp-portrange"] == expected
        assert await service.add()
        await service.refresh()
        assert service.model_dump(by_alias=True)["tcp-portrange"] == ["6666", "7777:1-1024"]

    async def test_firewall_custom_service_group(self, fmg):
        assert await fmg.get(ServiceGroup)
