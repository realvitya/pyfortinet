"""Custom service port ranges retain supplied values when serialized."""

import pytest

from pyfortinet.fmg_api.firewall import PortRange, ServiceCustom


@pytest.mark.parametrize("destination", [{"destination_start": "80"}, {"destination_end": "80"}])
@pytest.mark.parametrize("source", [{}, {"source_start": "123"}, {"source_end": "123"}])
def test_single_port_endpoint_round_trip(destination, source):
    ports = PortRange(**destination, **source)
    service = ServiceCustom(tcp_portrange=ports)
    expected = "80:123" if source else "80"
    payload = service.model_dump(by_alias=True, exclude_none=True)
    assert payload["tcp-portrange"] == [expected]


def test_explicit_port_ranges_round_trip():
    ports = PortRange(destination_start="80", destination_end="90", source_start="123", source_end="124")
    service = ServiceCustom(tcp_portrange=ports)
    assert service.model_dump(by_alias=True, exclude_none=True)["tcp-portrange"] == ["80-90:123-124"]
