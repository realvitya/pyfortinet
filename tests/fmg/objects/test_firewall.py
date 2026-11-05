"""Independent firewall CRUD tests with per-test resource ownership."""

import pytest

from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.firewall import Address, AddressGroup, PortRange, ServiceCustom, ServiceGroup


class TestObjects:
    def test_portrange(self):
        with pytest.raises(ValueError, match="Start port must be equal or less than end port"):
            PortRange(source_start="6666", source_end="5555")
        with pytest.raises(ValueError, match="Start port must be equal or less than end port"):
            PortRange(destination_start="6666", destination_end="5555")
        ports = PortRange(source_end="5555", destination_end="6666")
        assert ports.source_start == "5555" and ports.destination_start == "6666"


@pytest.mark.filterwarnings("ignore:Unverified")
class TestObjectsOnLab:
    def test_firewall_address(self, fmg, lab):
        address = lab.object(Address, "addr", subnet="10.0.0.0/24", allow_routing="disable")
        clone = lab.object(Address, "clone")
        assert address.add()
        assert address.clone(name=clone.name)
        wildcard = lab.object(Address, "wild", type="wildcard", wildcard="10.0.0.1 255.255.0.255")
        assert wildcard.add()
        assert (fmg.get(Address, F(name=wildcard.name))).first()
        assert wildcard.delete()
        loaded = (fmg.get(Address, F(name=address.name))).first()
        assert loaded.name == address.name
        loaded.subnet = "10.0.1.0/24"
        assert loaded.update()
        loaded.refresh()
        assert loaded.subnet == "10.0.1.0/24"
        assert loaded.delete()
        assert (fmg.get(Address, F(name=address.name))).first() is None
        assert address.set()
        assert address.delete()
        assert (fmg.get(Address, F(name=address.name))).first() is None

    def test_firewall_address_mapping(self, fmg, lab, lab_device):
        server = lab.object(Address, "server", subnet="10.0.0.1/32")
        assert server.add()
        server.dynamic_mapping = [Address(mapping__scope=lab_device.get_vdom_scope("root"), subnet="2.2.2.2")]
        assert server.update()
        server.refresh()
        assert any(mapping.subnet == "2.2.2.2/32" for mapping in server.dynamic_mapping)

    def test_firewall_address_group(self, fmg, lab):
        member1 = lab.object(Address, "addr1", subnet="10.0.0.1")
        member2 = lab.object(Address, "addr2", subnet="10.0.0.2")
        member3 = lab.object(Address, "addr3", subnet="10.0.0.3")
        assert member1.add()
        assert member2.add()
        assert member3.add()
        group1 = lab.object(AddressGroup, "grp1", member=[member1, member2])
        assert group1.add()
        group2 = lab.object(AddressGroup, "grp2", member=[member1, group1])
        assert group2.add()
        group1.member.append(member3)
        assert group1.update()
        group1.refresh()
        assert group1.member == [member1.name, member2.name, member3.name]
        found = (fmg.get(AddressGroup, F(name=group1.name) & F(member__contain=member1.name))).first()
        assert found.name == group1.name
        found = (
            fmg.get(
                AddressGroup, F(name=group2.name) & F(member__contain=member1.name) & F(member__contain=group1.name)
            )
        ).first()
        assert found.name == group2.name

    def test_firewall_custom_service(self, fmg, lab):
        services = fmg.get(ServiceCustom)
        assert services["QUAKE", "name"].name == "QUAKE" and services["QUAKE"].name == "QUAKE"
        with pytest.raises(AttributeError, match="invalid-key"):
            services["QUAKE", "invalid-key"]
        for ports, expected in [
            (PortRange(destination_end="6666"), ["6666"]),
            ("6666", ["6666"]),
            (["6666", "7777:1-1024"], ["6666", "7777:1-1024"]),
        ]:
            service = lab.object(ServiceCustom, "srv", tcp_portrange=ports)
            assert service.model_dump(by_alias=True)["tcp-portrange"] == expected
        assert service.add()
        service.refresh()
        assert service.model_dump(by_alias=True)["tcp-portrange"] == ["6666", "7777:1-1024"]

    def test_firewall_custom_service_group(self, fmg):
        assert fmg.get(ServiceGroup)
