"""Custom service port ranges retain supplied values when serialized."""

import pytest
from pydantic import ValidationError

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


@pytest.mark.parametrize("field", ["tcp_portrange", "udp_portrange", "sctp_portrange"])
@pytest.mark.parametrize("reverse", [False, True])
def test_mixed_port_input_order(field, reverse):
    ranges = [PortRange(destination_end="80"), "443:123"]
    expected = ["80", "443:123"]
    if reverse:
        ranges.reverse()
        expected.reverse()
    service = ServiceCustom(**{field: ranges})
    assert service.model_dump(by_alias=True, exclude_none=True)[field.replace("_", "-")] == expected


@pytest.mark.parametrize("field", ["tcp_portrange", "udp_portrange", "sctp_portrange"])
@pytest.mark.parametrize("invalid", ["invalid", "80oops", ["80", "bad"], ["80", 42]])
def test_invalid_port_ranges_are_not_silently_discarded(field, invalid):
    with pytest.raises(ValidationError):
        ServiceCustom(**{field: invalid})


def test_null_port_range_is_preserved():
    service = ServiceCustom(tcp_portrange=None)
    assert service.tcp_portrange is None
    assert "tcp-portrange" not in service.model_dump(by_alias=True, exclude_none=True)
