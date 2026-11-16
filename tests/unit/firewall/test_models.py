"""Offline model checks moved out of the lab tree."""

import pytest

from pyfortinet.fmg_api.firewall import PortRange


class TestAsyncObjects:
    def test_portrange(self):
        with pytest.raises(ValueError, match="Start port must be equal or less than end port"):
            PortRange(source_start="6666", source_end="5555")
        with pytest.raises(ValueError, match="Start port must be equal or less than end port"):
            PortRange(destination_start="6666", destination_end="5555")
        ports = PortRange(source_end="5555", destination_end="6666")
        assert ports.source_start == "5555" and ports.destination_start == "6666"


class TestSyncObjects:
    def test_portrange(self):
        with pytest.raises(ValueError, match="Start port must be equal or less than end port"):
            PortRange(source_start="6666", source_end="5555")
        with pytest.raises(ValueError, match="Start port must be equal or less than end port"):
            PortRange(destination_start="6666", destination_end="5555")
        ports = PortRange(source_end="5555", destination_end="6666")
        assert ports.source_start == "5555" and ports.destination_start == "6666"
