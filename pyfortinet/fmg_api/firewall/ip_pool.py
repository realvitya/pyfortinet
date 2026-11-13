"""IPPool schema for FMG 7.6.7, FortiOS 7.4 ADOM objects.

Static declarations; no private schema file is needed at runtime.
"""

from typing import Literal, Optional

from pydantic import AliasChoices, BaseModel, Field, field_validator

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.firewall._values import as_list, reference_names


class IPPoolDynamicMapping(BaseModel):
    """Fields for `pm.config.firewall.ippool.dynamic_mapping`; omitted values are not written."""

    mapping__scope: Optional[list[Scope]] = Field(
        None, validation_alias=AliasChoices("_scope", "mapping__scope"), serialization_alias="_scope"
    )
    add_nat64_route: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("add-nat64-route", "add_nat64_route"),
        serialization_alias="add-nat64-route",
        description=("Enable/disable adding NAT64 route."),
    )
    arp_intf: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("arp-intf", "arp_intf"),
        serialization_alias="arp-intf",
        description=(
            "Select an interface from available options that will reply to ARP requests. (If blank, any is selected)."
        ),
    )
    arp_reply: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("arp-reply", "arp_reply"),
        serialization_alias="arp-reply",
        description=(
            "Enable/disable replying to ARP requests when an IP Pool is added to a policy (default = enable)."
        ),
    )
    associated_interface: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("associated-interface", "associated_interface"),
        serialization_alias="associated-interface",
        description=("Associated interface name."),
    )
    block_size: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("block-size", "block_size"),
        serialization_alias="block-size",
        description=("Number of addresses in a block (64 - 4096, default = 128)."),
    )
    cgn_block_size: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cgn-block-size", "cgn_block_size"),
        serialization_alias="cgn-block-size",
        description=("Number of ports in a block(64 to 4096 in unit of 64, default = 128)."),
    )
    cgn_client_endip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("cgn-client-endip", "cgn_client_endip"),
        serialization_alias="cgn-client-endip",
        description=("Final client IPv4 address (inclusive) (format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."),
    )
    cgn_client_ipv6shift: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cgn-client-ipv6shift", "cgn_client_ipv6shift"),
        serialization_alias="cgn-client-ipv6shift",
        description=("IPv6 shift for fixed-allocation.(default 0)"),
    )
    cgn_client_startip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("cgn-client-startip", "cgn_client_startip"),
        serialization_alias="cgn-client-startip",
        description=("First client IPv4 address (inclusive) (format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."),
    )
    cgn_fixedalloc: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("cgn-fixedalloc", "cgn_fixedalloc"),
        serialization_alias="cgn-fixedalloc",
        description=("Enable/disable fixed-allocation mode."),
    )
    cgn_overload: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("cgn-overload", "cgn_overload"),
        serialization_alias="cgn-overload",
        description=("Enable/disable overload mode."),
    )
    cgn_port_end: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cgn-port-end", "cgn_port_end"),
        serialization_alias="cgn-port-end",
        description=("Ending public port can be allocated."),
    )
    cgn_port_start: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cgn-port-start", "cgn_port_start"),
        serialization_alias="cgn-port-start",
        description=("Starting public port can be allocated."),
    )
    cgn_spa: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("cgn-spa", "cgn_spa"),
        serialization_alias="cgn-spa",
        description=("Enable/disable single port allocation mode."),
    )
    client_prefix_length: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("client-prefix-length", "client_prefix_length"),
        serialization_alias="client-prefix-length",
    )
    comments: Optional[str] = Field(None, description=("Comment."))
    endip: Optional[str] = Field(
        None,
        description=(
            "Support meta variable Final IPv4 address (inclusive) in the range for the address pool "
            "(format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."
        ),
    )
    endport: Optional[int] = Field(
        None, description=("Final port number (inclusive) in the range for the address pool (Default: 65533).")
    )
    exclude_ip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("exclude-ip", "exclude_ip"),
        serialization_alias="exclude-ip",
        description=("Exclude IPs x.x.x.x."),
    )
    icmp_session_quota: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("icmp-session-quota", "icmp_session_quota"),
        serialization_alias="icmp-session-quota",
    )
    nat64: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable NAT64."))
    num_blocks_per_user: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("num-blocks-per-user", "num_blocks_per_user"),
        serialization_alias="num-blocks-per-user",
        description=("Number of addresses blocks that can be used by a user (1 to 128, default = 8)."),
    )
    pba_interim_log: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pba-interim-log", "pba_interim_log"),
        serialization_alias="pba-interim-log",
        description=(
            "Port block allocation interim logging interval (600 - 86400 seconds, default = 0 which "
            "disables interim logging)."
        ),
    )
    pba_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pba-timeout", "pba_timeout"),
        serialization_alias="pba-timeout",
        description=("Port block allocation timeout (seconds)."),
    )
    permit_any_host: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("permit-any-host", "permit_any_host"),
        serialization_alias="permit-any-host",
        description=("Enable/disable full cone NAT."),
    )
    port_per_user: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("port-per-user", "port_per_user"),
        serialization_alias="port-per-user",
        description=("Number of port for each user (32 - 60416, default = 0, which is auto)."),
    )
    privileged_port_use_pba: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("privileged-port-use-pba", "privileged_port_use_pba"),
        serialization_alias="privileged-port-use-pba",
    )
    source_endip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("source-endip", "source_endip"),
        serialization_alias="source-endip",
        description=(
            "Support meta variable Final IPv4 address (inclusive) in the range of the source addresses "
            "to be translated (format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."
        ),
    )
    source_prefix6: Optional[str] = Field(
        None, validation_alias=AliasChoices("source-prefix6", "source_prefix6"), serialization_alias="source-prefix6"
    )
    source_startip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("source-startip", "source_startip"),
        serialization_alias="source-startip",
        description=(
            "Support meta variable First IPv4 address (inclusive) in the range of the source addresses "
            "to be translated (format = xxx.xxx.xxx.xxx, default = 0.0.0.0)."
        ),
    )
    startip: Optional[str] = Field(
        None,
        description=(
            "Support meta variable First IPv4 address (inclusive) in the range for the address pool "
            "(format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."
        ),
    )
    startport: Optional[int] = Field(
        None, description=("First port number (inclusive) in the range for the address pool (Default: 5117).")
    )
    subnet_broadcast_in_ippool: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("subnet-broadcast-in-ippool", "subnet_broadcast_in_ippool"),
        serialization_alias="subnet-broadcast-in-ippool",
        description=(
            "Enable/disable inclusion of the subnetwork address and broadcast IP address in the NAT64 IP pool."
        ),
    )
    tcp_session_quota: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("tcp-session-quota", "tcp_session_quota"),
        serialization_alias="tcp-session-quota",
    )
    type: Optional[
        Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation", "cgn-resource-allocation"]
    ] = Field(
        None,
        description=(
            "IP pool type: overload, one-to-one, fixed-port-range, port-block-allocation, cgn-resource- "
            "allocation (hyperscale vdom only)"
        ),
    )
    udp_session_quota: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("udp-session-quota", "udp_session_quota"),
        serialization_alias="udp-session-quota",
    )
    utilization_alarm_clear: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("utilization-alarm-clear", "utilization_alarm_clear"),
        serialization_alias="utilization-alarm-clear",
        description=("Pool utilization alarm clear threshold (40-100)."),
    )
    utilization_alarm_raise: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("utilization-alarm-raise", "utilization_alarm_raise"),
        serialization_alias="utilization-alarm-raise",
        description=("Pool utilization alarm raise threshold (50-100)."),
    )

    @field_validator("mapping__scope", "exclude_ip", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator(
        "add_nat64_route",
        "arp_reply",
        "cgn_fixedalloc",
        "cgn_overload",
        "cgn_spa",
        "nat64",
        "permit_any_host",
        "privileged_port_use_pba",
        "subnet_broadcast_in_ippool",
        mode="before",
    )
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value


class IPPool(FMGObject):
    """Fields for `pm.config.firewall.ippool`; omitted values are not written."""

    _url: str = "/pm/config/{scope}/obj/firewall/ippool/{ippool}"
    _master_keys = {"ippool": "name"}

    add_nat64_route: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("add-nat64-route", "add_nat64_route"),
        serialization_alias="add-nat64-route",
        description=("Enable/disable adding NAT64 route."),
    )
    arp_intf: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("arp-intf", "arp_intf"),
        serialization_alias="arp-intf",
        description=(
            "Select an interface from available options that will reply to ARP requests. (If blank, any is selected)."
        ),
    )
    arp_reply: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("arp-reply", "arp_reply"),
        serialization_alias="arp-reply",
        description=(
            "Enable/disable replying to ARP requests when an IP Pool is added to a policy (default = enable)."
        ),
    )
    associated_interface: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("associated-interface", "associated_interface"),
        serialization_alias="associated-interface",
        description=("Associated interface name."),
    )
    block_size: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("block-size", "block_size"),
        serialization_alias="block-size",
        description=("Number of addresses in a block (64 - 4096, default = 128)."),
    )
    cgn_block_size: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cgn-block-size", "cgn_block_size"),
        serialization_alias="cgn-block-size",
        description=("Number of ports in a block(64 to 4096 in unit of 64, default = 128)."),
    )
    cgn_client_endip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("cgn-client-endip", "cgn_client_endip"),
        serialization_alias="cgn-client-endip",
        description=("Final client IPv4 address (inclusive) (format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."),
    )
    cgn_client_ipv6shift: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cgn-client-ipv6shift", "cgn_client_ipv6shift"),
        serialization_alias="cgn-client-ipv6shift",
        description=("IPv6 shift for fixed-allocation.(default 0)"),
    )
    cgn_client_startip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("cgn-client-startip", "cgn_client_startip"),
        serialization_alias="cgn-client-startip",
        description=("First client IPv4 address (inclusive) (format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."),
    )
    cgn_fixedalloc: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("cgn-fixedalloc", "cgn_fixedalloc"),
        serialization_alias="cgn-fixedalloc",
        description=("Enable/disable fixed-allocation mode."),
    )
    cgn_overload: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("cgn-overload", "cgn_overload"),
        serialization_alias="cgn-overload",
        description=("Enable/disable overload mode."),
    )
    cgn_port_end: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cgn-port-end", "cgn_port_end"),
        serialization_alias="cgn-port-end",
        description=("Ending public port can be allocated."),
    )
    cgn_port_start: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cgn-port-start", "cgn_port_start"),
        serialization_alias="cgn-port-start",
        description=("Starting public port can be allocated."),
    )
    cgn_spa: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("cgn-spa", "cgn_spa"),
        serialization_alias="cgn-spa",
        description=("Enable/disable single port allocation mode."),
    )
    comments: Optional[str] = Field(None, description=("Comment."))
    dynamic_mapping: Optional[list[IPPoolDynamicMapping]] = Field(None)
    endip: Optional[str] = Field(
        None,
        description=(
            "Support meta variable Final IPv4 address (inclusive) in the range for the address pool "
            "(format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."
        ),
    )
    endport: Optional[int] = Field(
        None, description=("Final port number (inclusive) in the range for the address pool (Default: 65533).")
    )
    exclude_ip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("exclude-ip", "exclude_ip"),
        serialization_alias="exclude-ip",
        description=("Exclude IPs x.x.x.x."),
    )
    name: Optional[str] = Field(None, description=("IP pool name."))
    nat64: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable NAT64."))
    num_blocks_per_user: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("num-blocks-per-user", "num_blocks_per_user"),
        serialization_alias="num-blocks-per-user",
        description=("Number of addresses blocks that can be used by a user (1 to 128, default = 8)."),
    )
    pba_interim_log: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pba-interim-log", "pba_interim_log"),
        serialization_alias="pba-interim-log",
        description=(
            "Port block allocation interim logging interval (600 - 86400 seconds, default = 0 which "
            "disables interim logging)."
        ),
    )
    pba_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pba-timeout", "pba_timeout"),
        serialization_alias="pba-timeout",
        description=("Port block allocation timeout (seconds)."),
    )
    permit_any_host: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("permit-any-host", "permit_any_host"),
        serialization_alias="permit-any-host",
        description=("Enable/disable full cone NAT."),
    )
    port_per_user: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("port-per-user", "port_per_user"),
        serialization_alias="port-per-user",
        description=("Number of port for each user (32 - 60416, default = 0, which is auto)."),
    )
    source_endip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("source-endip", "source_endip"),
        serialization_alias="source-endip",
        description=(
            "Support meta variable Final IPv4 address (inclusive) in the range of the source addresses "
            "to be translated (format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."
        ),
    )
    source_startip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("source-startip", "source_startip"),
        serialization_alias="source-startip",
        description=(
            "Support meta variable First IPv4 address (inclusive) in the range of the source addresses "
            "to be translated (format = xxx.xxx.xxx.xxx, default = 0.0.0.0)."
        ),
    )
    startip: Optional[str] = Field(
        None,
        description=(
            "Support meta variable First IPv4 address (inclusive) in the range for the address pool "
            "(format xxx.xxx.xxx.xxx, Default: 0.0.0.0)."
        ),
    )
    startport: Optional[int] = Field(
        None, description=("First port number (inclusive) in the range for the address pool (Default: 5117).")
    )
    subnet_broadcast_in_ippool: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("subnet-broadcast-in-ippool", "subnet_broadcast_in_ippool"),
        serialization_alias="subnet-broadcast-in-ippool",
        description=(
            "Enable/disable inclusion of the subnetwork address and broadcast IP address in the NAT64 IP pool."
        ),
    )
    type: Optional[
        Literal["overload", "one-to-one", "fixed-port-range", "port-block-allocation", "cgn-resource-allocation"]
    ] = Field(
        None,
        description=(
            "IP pool type: overload, one-to-one, fixed-port-range, port-block-allocation, cgn-resource- "
            "allocation (hyperscale vdom only)"
        ),
    )
    utilization_alarm_clear: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("utilization-alarm-clear", "utilization_alarm_clear"),
        serialization_alias="utilization-alarm-clear",
        description=("Pool utilization alarm clear threshold (40-100)."),
    )
    utilization_alarm_raise: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("utilization-alarm-raise", "utilization_alarm_raise"),
        serialization_alias="utilization-alarm-raise",
        description=("Pool utilization alarm raise threshold (50-100)."),
    )

    @field_validator("dynamic_mapping", "exclude_ip", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator("arp_intf", "associated_interface", mode="before")
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)

    @field_validator(
        "add_nat64_route",
        "arp_reply",
        "cgn_fixedalloc",
        "cgn_overload",
        "cgn_spa",
        "nat64",
        "permit_any_host",
        "subnet_broadcast_in_ippool",
        mode="before",
    )
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value
