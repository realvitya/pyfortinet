"""Additional interface fields from FMG 7.6.7, FortiOS 7.4 device configuration.

Static declarations: the source schema is not required at runtime. Fields remain optional
because the same models represent partial GET replies and ADD/SET/UPDATE payloads.
"""

from typing import Literal, Optional

from pydantic import AliasChoices, BaseModel, Field


class InterfaceClientOptions(BaseModel):
    """Fields for `pm.config.system.interface.client-options`."""

    code: Optional[int] = Field(None, description="DHCP client option code.")
    id: Optional[int] = Field(None, description="ID.")
    ip: Optional[list[str]] = Field(None, description="DHCP option IPs.")
    type: Optional[Literal["hex", "string", "ip", "fqdn"]] = Field(None, description="DHCP client option type.")
    value: Optional[str] = Field(None, description="DHCP client option value.")


class InterfaceDhcpSnoopingServerList(BaseModel):
    """Fields for `pm.config.system.interface.dhcp-snooping-server-list`."""

    name: Optional[str] = Field(None, description="DHCP server name.")
    server_ip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("server-ip", "server_ip"),
        serialization_alias="server-ip",
        description="IP address for DHCP server.",
    )


class InterfaceEgressQueues(BaseModel):
    """Fields for `pm.config.system.interface.egress-queues`."""

    cos0: Optional[list[str]] = Field(None, description="CoS profile name for CoS 0.")
    cos1: Optional[list[str]] = Field(None, description="CoS profile name for CoS 1.")
    cos2: Optional[list[str]] = Field(None, description="CoS profile name for CoS 2.")
    cos3: Optional[list[str]] = Field(None, description="CoS profile name for CoS 3.")
    cos4: Optional[list[str]] = Field(None, description="CoS profile name for CoS 4.")
    cos5: Optional[list[str]] = Field(None, description="CoS profile name for CoS 5.")
    cos6: Optional[list[str]] = Field(None, description="CoS profile name for CoS 6.")
    cos7: Optional[list[str]] = Field(None, description="CoS profile name for CoS 7.")


class InterfaceIpv6Dhcp6IapdList(BaseModel):
    """Fields for `pm.config.system.interface.ipv6.dhcp6-iapd-list`."""

    iaid: Optional[int] = Field(None, description="Identity association identifier.")
    prefix_hint: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("prefix-hint", "prefix_hint"),
        serialization_alias="prefix-hint",
        description="DHCPv6 prefix that will be used as a hint to the upstream DHCPv6 server.",
    )
    prefix_hint_plt: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("prefix-hint-plt", "prefix_hint_plt"),
        serialization_alias="prefix-hint-plt",
        description="DHCPv6 prefix hint preferred life time (sec), 0 means unlimited lease time.",
    )
    prefix_hint_vlt: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("prefix-hint-vlt", "prefix_hint_vlt"),
        serialization_alias="prefix-hint-vlt",
        description="DHCPv6 prefix hint valid life time (sec).",
    )


class InterfaceIpv6Ip6DelegatedPrefixList(BaseModel):
    """Fields for `pm.config.system.interface.ipv6.ip6-delegated-prefix-list`."""

    autonomous_flag: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("autonomous-flag", "autonomous_flag"),
        serialization_alias="autonomous-flag",
        description="Enable/disable the autonomous flag.",
    )
    delegated_prefix_iaid: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("delegated-prefix-iaid", "delegated_prefix_iaid"),
        serialization_alias="delegated-prefix-iaid",
        description="IAID of obtained delegated-prefix from the upstream interface.",
    )
    onlink_flag: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("onlink-flag", "onlink_flag"),
        serialization_alias="onlink-flag",
        description="Enable/disable the onlink flag.",
    )
    prefix_id: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("prefix-id", "prefix_id"),
        serialization_alias="prefix-id",
        description="Prefix ID.",
    )
    rdnss: Optional[list[str]] = Field(None, description="Recursive DNS server option.")
    rdnss_service: Optional[Literal["delegated", "default", "specify"]] = Field(
        None,
        validation_alias=AliasChoices("rdnss-service", "rdnss_service"),
        serialization_alias="rdnss-service",
        description="Recursive DNS service option.",
    )
    subnet: Optional[str] = Field(None, description="Add subnet ID to routing prefix.")
    upstream_interface: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("upstream-interface", "upstream_interface"),
        serialization_alias="upstream-interface",
        description="Name of the interface that provides delegated information.",
    )


class InterfaceIpv6Ip6ExtraAddr(BaseModel):
    """Fields for `pm.config.system.interface.ipv6.ip6-extra-addr`."""

    prefix: Optional[str] = Field(None, description="IPv6 address prefix.")


class InterfaceIpv6Ip6PrefixList(BaseModel):
    """Fields for `pm.config.system.interface.ipv6.ip6-prefix-list`."""

    autonomous_flag: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("autonomous-flag", "autonomous_flag"),
        serialization_alias="autonomous-flag",
        description="Enable/disable the autonomous flag.",
    )
    dnssl: Optional[list[str]] = Field(None, description="DNS search list option.")
    onlink_flag: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("onlink-flag", "onlink_flag"),
        serialization_alias="onlink-flag",
        description="Enable/disable the onlink flag.",
    )
    preferred_life_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("preferred-life-time", "preferred_life_time"),
        serialization_alias="preferred-life-time",
        description="Preferred life time (sec).",
    )
    prefix: Optional[str] = Field(None, description="IPv6 prefix.")
    rdnss: Optional[list[str]] = Field(None, description="Recursive DNS server option.")
    valid_life_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("valid-life-time", "valid_life_time"),
        serialization_alias="valid-life-time",
        description="Valid life time (sec).",
    )


class InterfaceIpv6Vrrp6(BaseModel):
    """Fields for `pm.config.system.interface.ipv6.vrrp6`."""

    accept_mode: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("accept-mode", "accept_mode"),
        serialization_alias="accept-mode",
        description="Enable/disable accept mode.",
    )
    adv_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("adv-interval", "adv_interval"),
        serialization_alias="adv-interval",
        description="Advertisement interval (1 - 255 seconds).",
    )
    ignore_default_route: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ignore-default-route", "ignore_default_route"),
        serialization_alias="ignore-default-route",
        description="Enable/disable ignoring of default route when checking destination.",
    )
    preempt: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable preempt mode.")
    priority: Optional[int] = Field(None, description="Priority of the virtual router (1 - 255).")
    start_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("start-time", "start_time"),
        serialization_alias="start-time",
        description="Startup time (1 - 255 seconds).",
    )
    status: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable VRRP.")
    vrdst6: Optional[list[str]] = Field(None, description="Monitor the route to this destination.")
    vrgrp: Optional[int] = Field(None, description="VRRP group ID (1 - 65535).")
    vrid: Optional[int] = Field(None, description="Virtual router identifier (1 - 255).")
    vrip6: Optional[str] = Field(None, description="IPv6 address of the virtual router.")


class InterfaceIpv6(BaseModel):
    """Fields for `pm.config.system.interface.ipv6`."""

    autoconf: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable address auto config.")
    cli_conn6_status: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("cli-conn6-status", "cli_conn6_status"),
        serialization_alias="cli-conn6-status",
    )
    dhcp6_client_options: Optional[list[Literal["rapid", "iapd", "iana"]]] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-client-options", "dhcp6_client_options"),
        serialization_alias="dhcp6-client-options",
    )
    dhcp6_iapd_list: Optional[list[InterfaceIpv6Dhcp6IapdList]] = Field(
        None, validation_alias=AliasChoices("dhcp6-iapd-list", "dhcp6_iapd_list"), serialization_alias="dhcp6-iapd-list"
    )
    dhcp6_information_request: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-information-request", "dhcp6_information_request"),
        serialization_alias="dhcp6-information-request",
        description="Enable/disable DHCPv6 information request.",
    )
    dhcp6_prefix_delegation: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-prefix-delegation", "dhcp6_prefix_delegation"),
        serialization_alias="dhcp6-prefix-delegation",
        description="Enable/disable DHCPv6 prefix delegation.",
    )
    dhcp6_relay_interface_id: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-relay-interface-id", "dhcp6_relay_interface_id"),
        serialization_alias="dhcp6-relay-interface-id",
        description="DHCP6 relay interface ID.",
    )
    dhcp6_relay_ip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-relay-ip", "dhcp6_relay_ip"),
        serialization_alias="dhcp6-relay-ip",
        description="DHCPv6 relay IP address.",
    )
    dhcp6_relay_service: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-relay-service", "dhcp6_relay_service"),
        serialization_alias="dhcp6-relay-service",
        description="Enable/disable DHCPv6 relay.",
    )
    dhcp6_relay_source_interface: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-relay-source-interface", "dhcp6_relay_source_interface"),
        serialization_alias="dhcp6-relay-source-interface",
        description="Enable/disable use of address on this interface as the source address of the relay message.",
    )
    dhcp6_relay_source_ip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-relay-source-ip", "dhcp6_relay_source_ip"),
        serialization_alias="dhcp6-relay-source-ip",
        description="IPv6 address used by the DHCP6 relay as its source IP.",
    )
    dhcp6_relay_type: Optional[Literal["regular"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp6-relay-type", "dhcp6_relay_type"),
        serialization_alias="dhcp6-relay-type",
        description="DHCPv6 relay type.",
    )
    icmp6_send_redirect: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("icmp6-send-redirect", "icmp6_send_redirect"),
        serialization_alias="icmp6-send-redirect",
        description="Enable/disable sending of ICMPv6 redirects.",
    )
    interface_identifier: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("interface-identifier", "interface_identifier"),
        serialization_alias="interface-identifier",
        description="IPv6 interface identifier.",
    )
    ip6_address: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-address", "ip6_address"),
        serialization_alias="ip6-address",
        description="Primary IPv6 address prefix. Syntax: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx.",
    )
    ip6_allowaccess: Optional[list[Literal["https", "ping", "ssh", "snmp", "http", "telnet", "fgfm", "fabric"]]] = (
        Field(
            None,
            validation_alias=AliasChoices("ip6-allowaccess", "ip6_allowaccess"),
            serialization_alias="ip6-allowaccess",
            description="Allow management access to the interface.",
        )
    )
    ip6_default_life: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-default-life", "ip6_default_life"),
        serialization_alias="ip6-default-life",
        description="Default life (sec).",
    )
    ip6_delegated_prefix_iaid: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-delegated-prefix-iaid", "ip6_delegated_prefix_iaid"),
        serialization_alias="ip6-delegated-prefix-iaid",
        description="IAID of obtained delegated-prefix from the upstream interface.",
    )
    ip6_delegated_prefix_list: Optional[list[InterfaceIpv6Ip6DelegatedPrefixList]] = Field(
        None,
        validation_alias=AliasChoices("ip6-delegated-prefix-list", "ip6_delegated_prefix_list"),
        serialization_alias="ip6-delegated-prefix-list",
    )
    ip6_dns_server_override: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ip6-dns-server-override", "ip6_dns_server_override"),
        serialization_alias="ip6-dns-server-override",
        description="Enable/disable using the DNS server acquired by DHCP.",
    )
    ip6_extra_addr: Optional[list[InterfaceIpv6Ip6ExtraAddr]] = Field(
        None, validation_alias=AliasChoices("ip6-extra-addr", "ip6_extra_addr"), serialization_alias="ip6-extra-addr"
    )
    ip6_hop_limit: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-hop-limit", "ip6_hop_limit"),
        serialization_alias="ip6-hop-limit",
        description="Hop limit (0 means unspecified).",
    )
    ip6_link_mtu: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-link-mtu", "ip6_link_mtu"),
        serialization_alias="ip6-link-mtu",
        description="IPv6 link MTU.",
    )
    ip6_manage_flag: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ip6-manage-flag", "ip6_manage_flag"),
        serialization_alias="ip6-manage-flag",
        description="Enable/disable the managed flag.",
    )
    ip6_max_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-max-interval", "ip6_max_interval"),
        serialization_alias="ip6-max-interval",
        description="IPv6 maximum interval (4 to 1800 sec).",
    )
    ip6_min_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-min-interval", "ip6_min_interval"),
        serialization_alias="ip6-min-interval",
        description="IPv6 minimum interval (3 to 1350 sec).",
    )
    ip6_mode: Optional[Literal["static", "dhcp", "pppoe", "delegated"]] = Field(
        None,
        validation_alias=AliasChoices("ip6-mode", "ip6_mode"),
        serialization_alias="ip6-mode",
        description="Addressing mode (static, DHCP, delegated).",
    )
    ip6_other_flag: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ip6-other-flag", "ip6_other_flag"),
        serialization_alias="ip6-other-flag",
        description="Enable/disable the other IPv6 flag.",
    )
    ip6_prefix_list: Optional[list[InterfaceIpv6Ip6PrefixList]] = Field(
        None, validation_alias=AliasChoices("ip6-prefix-list", "ip6_prefix_list"), serialization_alias="ip6-prefix-list"
    )
    ip6_prefix_mode: Optional[Literal["dhcp6", "ra"]] = Field(
        None,
        validation_alias=AliasChoices("ip6-prefix-mode", "ip6_prefix_mode"),
        serialization_alias="ip6-prefix-mode",
        description="Assigning a prefix from DHCP or RA.",
    )
    ip6_reachable_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-reachable-time", "ip6_reachable_time"),
        serialization_alias="ip6-reachable-time",
        description="IPv6 reachable time (milliseconds; 0 means unspecified).",
    )
    ip6_retrans_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-retrans-time", "ip6_retrans_time"),
        serialization_alias="ip6-retrans-time",
        description="IPv6 retransmit time (milliseconds; 0 means unspecified).",
    )
    ip6_send_adv: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ip6-send-adv", "ip6_send_adv"),
        serialization_alias="ip6-send-adv",
        description="Enable/disable sending advertisements about the interface.",
    )
    ip6_subnet: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-subnet", "ip6_subnet"),
        serialization_alias="ip6-subnet",
        description="Subnet to routing prefix. Syntax: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx/xxx.",
    )
    ip6_upstream_interface: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ip6-upstream-interface", "ip6_upstream_interface"),
        serialization_alias="ip6-upstream-interface",
        description="Interface name providing delegated information.",
    )
    nd_cert: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("nd-cert", "nd_cert"),
        serialization_alias="nd-cert",
        description="Neighbor discovery certificate.",
    )
    nd_cga_modifier: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("nd-cga-modifier", "nd_cga_modifier"),
        serialization_alias="nd-cga-modifier",
        description="Neighbor discovery CGA modifier.",
    )
    nd_mode: Optional[Literal["basic", "SEND-compatible"]] = Field(
        None,
        validation_alias=AliasChoices("nd-mode", "nd_mode"),
        serialization_alias="nd-mode",
        description="Neighbor discovery mode.",
    )
    nd_security_level: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("nd-security-level", "nd_security_level"),
        serialization_alias="nd-security-level",
        description="Neighbor discovery security level (0 - 7; 0 = least secure, default = 0).",
    )
    nd_timestamp_delta: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("nd-timestamp-delta", "nd_timestamp_delta"),
        serialization_alias="nd-timestamp-delta",
        description="Neighbor discovery timestamp delta value (1 - 3600 sec; default = 300).",
    )
    nd_timestamp_fuzz: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("nd-timestamp-fuzz", "nd_timestamp_fuzz"),
        serialization_alias="nd-timestamp-fuzz",
        description="Neighbor discovery timestamp fuzz factor (1 - 60 sec; default = 1).",
    )
    ra_send_mtu: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ra-send-mtu", "ra_send_mtu"),
        serialization_alias="ra-send-mtu",
        description="Enable/disable sending link MTU in RA packet.",
    )
    unique_autoconf_addr: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("unique-autoconf-addr", "unique_autoconf_addr"),
        serialization_alias="unique-autoconf-addr",
        description="Enable/disable unique auto config address.",
    )
    vrip6_link_local: Optional[str] = Field(None, description="Link-local IPv6 address of virtual router.")
    vrrp_virtual_mac6: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("vrrp-virtual-mac6", "vrrp_virtual_mac6"),
        serialization_alias="vrrp-virtual-mac6",
        description="Enable/disable virtual MAC for VRRP.",
    )
    vrrp6: Optional[list[InterfaceIpv6Vrrp6]] = Field(None)


class InterfaceL2tpClientSettings(BaseModel):
    """Fields for `pm.config.system.interface.l2tp-client-settings`."""

    auth_type: Optional[Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]] = Field(
        None,
        validation_alias=AliasChoices("auth-type", "auth_type"),
        serialization_alias="auth-type",
        description="L2TP authentication type.",
    )
    defaultgw: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable default gateway.")
    distance: Optional[int] = Field(None, description="Distance of learned routes.")
    hello_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("hello-interval", "hello_interval"),
        serialization_alias="hello-interval",
        description="L2TP hello message interval in seconds (0 - 3600 sec, default = 60).",
    )
    ip: Optional[list[str]] = Field(None)
    mtu: Optional[int] = Field(None, description="L2TP MTU.")
    password: Optional[list[str]] = Field(None, description="L2TP password.", repr=False)
    peer_host: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("peer-host", "peer_host"),
        serialization_alias="peer-host",
        description="L2TP peer host address.",
    )
    peer_mask: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("peer-mask", "peer_mask"),
        serialization_alias="peer-mask",
        description="L2TP peer mask.",
    )
    peer_port: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("peer-port", "peer_port"),
        serialization_alias="peer-port",
        description="L2TP peer port number.",
    )
    priority: Optional[int] = Field(None, description="Priority of learned routes.")
    user: Optional[str] = Field(None, description="L2TP user name.")


class InterfaceMirroringFilter(BaseModel):
    """Fields for `pm.config.system.interface.mirroring-filter`."""

    dbg_dump: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("dbg-dump", "dbg_dump"),
        serialization_alias="dbg-dump",
        description="Debug mirroring filter, driver dump data/mask pdq.",
    )
    filter_dport: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("filter-dport", "filter_dport"),
        serialization_alias="filter-dport",
        description="Destinatin port of mirroring filter.",
    )
    filter_dstip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("filter-dstip", "filter_dstip"),
        serialization_alias="filter-dstip",
        description="Destinatin IP and mask of mirroring filter.",
    )
    filter_protocol: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("filter-protocol", "filter_protocol"),
        serialization_alias="filter-protocol",
        description="Protocol of mirroring filter.",
    )
    filter_sport: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("filter-sport", "filter_sport"),
        serialization_alias="filter-sport",
        description="Source port of mirroring filter.",
    )
    filter_srcip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("filter-srcip", "filter_srcip"),
        serialization_alias="filter-srcip",
        description="Source IP and mask of mirroring filter.",
    )


class InterfacePhySetting(BaseModel):
    """Fields for `pm.config.system.interface.phy-setting`."""

    signal_ok_threshold_value: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("signal-ok-threshold-value", "signal_ok_threshold_value"),
        serialization_alias="signal-ok-threshold-value",
        description="Signal-ok-threshold value(0 - 12).",
    )


class InterfaceSecondaryip(BaseModel):
    """Fields for `pm.config.system.interface.secondaryip`."""

    allowaccess: Optional[
        list[
            Literal[
                "https",
                "ping",
                "ssh",
                "snmp",
                "http",
                "telnet",
                "fgfm",
                "radius-acct",
                "probe-response",
                "dnp",
                "ftm",
                "fabric",
                "speed-test",
                "icond",
            ]
        ]
    ] = Field(None, description="Management access settings for the secondary IP address.")
    id: Optional[int] = Field(None, description="ID.")
    ip: Optional[list[str]] = Field(None, description="Secondary IP address of the interface.")
    secip_relay_ip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("secip-relay-ip", "secip_relay_ip"),
        serialization_alias="secip-relay-ip",
        description="DHCP relay IP address.",
    )


class InterfaceTagging(BaseModel):
    """Fields for `pm.config.system.interface.tagging`."""

    category: Optional[list[str]] = Field(None, description="Tag category.")
    name: Optional[str] = Field(None, description="Tagging entry name.")
    tags: Optional[list[str]] = Field(None, description="Tags.")


class InterfaceVrrpProxyArp(BaseModel):
    """Fields for `pm.config.system.interface.vrrp.proxy-arp`."""

    id: Optional[int] = Field(None, description="ID.")
    ip: Optional[str] = Field(None, description="Set IP addresses of proxy ARP.")


class InterfaceVrrp(BaseModel):
    """Fields for `pm.config.system.interface.vrrp`."""

    accept_mode: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("accept-mode", "accept_mode"),
        serialization_alias="accept-mode",
        description="Enable/disable accept mode.",
    )
    adv_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("adv-interval", "adv_interval"),
        serialization_alias="adv-interval",
        description="Advertisement interval (1 - 255 seconds).",
    )
    ignore_default_route: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ignore-default-route", "ignore_default_route"),
        serialization_alias="ignore-default-route",
        description="Enable/disable ignoring of default route when checking destination.",
    )
    preempt: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable preempt mode.")
    priority: Optional[int] = Field(None, description="Priority of the virtual router (1 - 255).")
    proxy_arp: Optional[list[InterfaceVrrpProxyArp]] = Field(
        None, validation_alias=AliasChoices("proxy-arp", "proxy_arp"), serialization_alias="proxy-arp"
    )
    start_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("start-time", "start_time"),
        serialization_alias="start-time",
        description="Startup time (1 - 255 seconds).",
    )
    status: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable this VRRP configuration.")
    version: Optional[Literal["2", "3"]] = Field(None, description="VRRP version.")
    vrdst: Optional[list[str]] = Field(None, description="Monitor the route to this destination.")
    vrdst_priority: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("vrdst-priority", "vrdst_priority"),
        serialization_alias="vrdst-priority",
        description="Priority of the virtual router when the virtual router destination becomes unreachable (0 - 254).",
    )
    vrgrp: Optional[int] = Field(None, description="VRRP group ID (1 - 65535).")
    vrid: Optional[int] = Field(None, description="Virtual router identifier (1 - 255).")
    vrip: Optional[str] = Field(None, description="IP address of the virtual router.")


class InterfaceWifiNetworks(BaseModel):
    """Fields for `pm.config.system.interface.wifi-networks`."""

    id: Optional[int] = Field(None, description="ID.")
    obsolete_security_options: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("obsolete-security-options", "obsolete_security_options"),
        serialization_alias="obsolete-security-options",
        description="Enable/disable obsolete security options.",
    )
    wifi_ca_certificate: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("wifi-ca-certificate", "wifi_ca_certificate"),
        serialization_alias="wifi-ca-certificate",
        description="CA certificate for WPA2/WPA3-ENTERPRISE.",
    )
    wifi_client_certificate: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("wifi-client-certificate", "wifi_client_certificate"),
        serialization_alias="wifi-client-certificate",
        description="Client certificate for WPA2/WPA3-ENTERPRISE.",
    )
    wifi_eap_type: Optional[Literal["tls", "peap", "both"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-eap-type", "wifi_eap_type"),
        serialization_alias="wifi-eap-type",
        description="WPA2/WPA3-ENTERPRISE EAP Method.",
    )
    wifi_encrypt: Optional[Literal["TKIP", "AES"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-encrypt", "wifi_encrypt"),
        serialization_alias="wifi-encrypt",
        description="Data encryption.",
    )
    wifi_key: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("wifi-key", "wifi_key"),
        serialization_alias="wifi-key",
        description="WiFi WEP Key.",
    )
    wifi_keyindex: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("wifi-keyindex", "wifi_keyindex"),
        serialization_alias="wifi-keyindex",
        description="WEP key index (1 - 4).",
    )
    wifi_passphrase: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("wifi-passphrase", "wifi_passphrase"),
        serialization_alias="wifi-passphrase",
        description="WiFi pre-shared key for WPA-PSK or password for WPA3-SAE and WPA2/WPA3-ENTERPRISE.",
    )
    wifi_private_key: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-private-key", "wifi_private_key"),
        serialization_alias="wifi-private-key",
        description="Private key for WPA2/WPA3-ENTERPRISE.",
    )
    wifi_private_key_password: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("wifi-private-key-password", "wifi_private_key_password"),
        serialization_alias="wifi-private-key-password",
        description="Password for private key file for WPA2/WPA3-ENTERPRISE.",
        repr=False,
    )
    wifi_security: Optional[
        Literal[
            "wep64",
            "wep128",
            "open",
            "wpa-personal",
            "wpa-enterprise",
            "wpa-only-personal",
            "wpa2-only-personal",
            "owe",
            "wpa3-sae",
        ]
    ] = Field(
        None,
        validation_alias=AliasChoices("wifi-security", "wifi_security"),
        serialization_alias="wifi-security",
        description="Wireless access security of SSID.",
    )
    wifi_ssid: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-ssid", "wifi_ssid"),
        serialization_alias="wifi-ssid",
        description="IEEE 802.11 Service Set Identifier.",
    )
    wifi_username: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-username", "wifi_username"),
        serialization_alias="wifi-username",
        description="Username for WPA2/WPA3-ENTERPRISE.",
    )


class InterfaceFields(BaseModel):
    """Fields for `pm.config.system.interface`."""

    ac_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ac-name", "ac_name"),
        serialization_alias="ac-name",
        description="PPPoE server name.",
    )
    aggregate: Optional[str] = Field(None)
    aggregate_type: Optional[Literal["physical", "vxlan"]] = Field(
        None,
        validation_alias=AliasChoices("aggregate-type", "aggregate_type"),
        serialization_alias="aggregate-type",
        description="Type of aggregation.",
    )
    algorithm: Optional[Literal["L2", "L3", "L4", "Source-MAC"]] = Field(
        None, description="Frame distribution algorithm."
    )
    annex: Optional[Literal["a", "b", "j", "bjm", "i", "al", "m", "aijlm", "bj"]] = Field(
        None, description="Set xDSL annex type."
    )
    ap_discover: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ap-discover", "ap_discover"),
        serialization_alias="ap-discover",
        description="Enable/disable automatic registration of unknown FortiAP devices.",
    )
    atm_protocol: Optional[Literal["none", "ipoa"]] = Field(
        None,
        validation_alias=AliasChoices("atm-protocol", "atm_protocol"),
        serialization_alias="atm-protocol",
        description="ATM protocol.",
    )
    auth_cert: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("auth-cert", "auth_cert"),
        serialization_alias="auth-cert",
        description="HTTPS server certificate.",
    )
    auth_portal_addr: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("auth-portal-addr", "auth_portal_addr"),
        serialization_alias="auth-portal-addr",
        description="Address of captive portal.",
    )
    auth_type: Optional[Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]] = Field(
        None,
        validation_alias=AliasChoices("auth-type", "auth_type"),
        serialization_alias="auth-type",
        description="PPP authentication type to use.",
    )
    auto_auth_extension_device: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("auto-auth-extension-device", "auto_auth_extension_device"),
        serialization_alias="auto-auth-extension-device",
        description="Enable/disable automatic authorization of dedicated Fortinet extension device on this interface.",
    )
    bandwidth_measure_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("bandwidth-measure-time", "bandwidth_measure_time"),
        serialization_alias="bandwidth-measure-time",
        description="Bandwidth measure time.",
    )
    bfd_desired_min_tx: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("bfd-desired-min-tx", "bfd_desired_min_tx"),
        serialization_alias="bfd-desired-min-tx",
        description="BFD desired minimal transmit interval.",
    )
    bfd_detect_mult: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("bfd-detect-mult", "bfd_detect_mult"),
        serialization_alias="bfd-detect-mult",
        description="BFD detection multiplier.",
    )
    bfd_required_min_rx: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("bfd-required-min-rx", "bfd_required_min_rx"),
        serialization_alias="bfd-required-min-rx",
        description="BFD required minimal receive interval.",
    )
    captive_portal: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("captive-portal", "captive_portal"),
        serialization_alias="captive-portal",
        description="Enable/disable captive portal.",
    )
    cli_conn_status: Optional[int] = Field(
        None, validation_alias=AliasChoices("cli-conn-status", "cli_conn_status"), serialization_alias="cli-conn-status"
    )
    client_options: Optional[list[InterfaceClientOptions]] = Field(
        None, validation_alias=AliasChoices("client-options", "client_options"), serialization_alias="client-options"
    )
    color: Optional[int] = Field(None, description="Color of icon on the GUI.")
    dedicated_to: Optional[Literal["none", "management"]] = Field(
        None,
        validation_alias=AliasChoices("dedicated-to", "dedicated_to"),
        serialization_alias="dedicated-to",
        description="Configure interface for single purpose.",
    )
    default_purdue_level: Optional[Literal["1", "2", "3", "4", "5", "1.5", "2.5", "3.5", "5.5"]] = Field(
        None,
        validation_alias=AliasChoices("default-purdue-level", "default_purdue_level"),
        serialization_alias="default-purdue-level",
        description="default purdue level of device detected on this interface.",
    )
    defaultgw: Optional[Literal["disable", "enable"]] = Field(
        None, description="Enable to get the gateway IP from the DHCP or PPPoE server."
    )
    detected_peer_mtu: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("detected-peer-mtu", "detected_peer_mtu"),
        serialization_alias="detected-peer-mtu",
    )
    device_identification: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("device-identification", "device_identification"),
        serialization_alias="device-identification",
        description=(
            "Enable/disable passively gathering of device identity information about the devices on the "
            "network connected to this interface."
        ),
    )
    device_user_identification: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("device-user-identification", "device_user_identification"),
        serialization_alias="device-user-identification",
        description="Enable/disable passive gathering of user identity information about users on this interface.",
    )
    dhcp_broadcast_flag: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-broadcast-flag", "dhcp_broadcast_flag"),
        serialization_alias="dhcp-broadcast-flag",
        description=(
            "Enable/disable setting of the broadcast flag in messages sent by the DHCP client (default = enable)."
        ),
    )
    dhcp_classless_route_addition: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-classless-route-addition", "dhcp_classless_route_addition"),
        serialization_alias="dhcp-classless-route-addition",
        description="Enable/disable addition of classless static routes retrieved from DHCP server.",
    )
    dhcp_client_identifier: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dhcp-client-identifier", "dhcp_client_identifier"),
        serialization_alias="dhcp-client-identifier",
        description="DHCP client identifier.",
    )
    dhcp_relay_agent_option: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-agent-option", "dhcp_relay_agent_option"),
        serialization_alias="dhcp-relay-agent-option",
        description="Enable/disable DHCP relay agent option.",
    )
    dhcp_relay_allow_no_end_option: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-allow-no-end-option", "dhcp_relay_allow_no_end_option"),
        serialization_alias="dhcp-relay-allow-no-end-option",
        description="Enable/disable relaying DHCP messages with no end option.",
    )
    dhcp_relay_circuit_id: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-circuit-id", "dhcp_relay_circuit_id"),
        serialization_alias="dhcp-relay-circuit-id",
        description="DHCP relay circuit ID.",
    )
    dhcp_relay_interface: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-interface", "dhcp_relay_interface"),
        serialization_alias="dhcp-relay-interface",
        description="Specify outgoing interface to reach server.",
    )
    dhcp_relay_interface_select_method: Optional[Literal["auto", "sdwan", "specify"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-interface-select-method", "dhcp_relay_interface_select_method"),
        serialization_alias="dhcp-relay-interface-select-method",
        description="Specify how to select outgoing interface to reach server.",
    )
    dhcp_relay_ip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-ip", "dhcp_relay_ip"),
        serialization_alias="dhcp-relay-ip",
        description="DHCP relay IP address.",
    )
    dhcp_relay_link_selection: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-link-selection", "dhcp_relay_link_selection"),
        serialization_alias="dhcp-relay-link-selection",
        description="DHCP relay link selection.",
    )
    dhcp_relay_request_all_server: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-request-all-server", "dhcp_relay_request_all_server"),
        serialization_alias="dhcp-relay-request-all-server",
        description="Enable/disable sending of DHCP requests to all servers.",
    )
    dhcp_relay_service: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-service", "dhcp_relay_service"),
        serialization_alias="dhcp-relay-service",
        description="Enable/disable allowing this interface to act as a DHCP relay.",
    )
    dhcp_relay_source_ip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-source-ip", "dhcp_relay_source_ip"),
        serialization_alias="dhcp-relay-source-ip",
        description="IP address used by the DHCP relay as its source IP.",
    )
    dhcp_relay_type: Optional[Literal["regular", "ipsec"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-relay-type", "dhcp_relay_type"),
        serialization_alias="dhcp-relay-type",
        description="DHCP relay type (regular or IPsec).",
    )
    dhcp_renew_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("dhcp-renew-time", "dhcp_renew_time"),
        serialization_alias="dhcp-renew-time",
        description="DHCP renew time in seconds (300-604800), 0 means use the renew time provided by the server.",
    )
    dhcp_smart_relay: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-smart-relay", "dhcp_smart_relay"),
        serialization_alias="dhcp-smart-relay",
        description="Enable/disable DHCP smart relay.",
    )
    dhcp_snooping_server_list: Optional[list[InterfaceDhcpSnoopingServerList]] = Field(
        None,
        validation_alias=AliasChoices("dhcp-snooping-server-list", "dhcp_snooping_server_list"),
        serialization_alias="dhcp-snooping-server-list",
    )
    disc_retry_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("disc-retry-timeout", "disc_retry_timeout"),
        serialization_alias="disc-retry-timeout",
        description="Time in seconds to wait before retrying to start a PPPoE discovery, 0 means no timeout.",
    )
    distance: Optional[int] = Field(
        None, description="Distance for routes learned through PPPoE or DHCP, lower distance indicates preferred route."
    )
    dns_server_override: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("dns-server-override", "dns_server_override"),
        serialization_alias="dns-server-override",
        description="Enable/disable use DNS acquired by DHCP or PPPoE.",
    )
    dns_server_protocol: Optional[list[Literal["cleartext", "dot", "doh"]]] = Field(
        None,
        validation_alias=AliasChoices("dns-server-protocol", "dns_server_protocol"),
        serialization_alias="dns-server-protocol",
        description="DNS transport protocols.",
    )
    drop_fragment: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("drop-fragment", "drop_fragment"),
        serialization_alias="drop-fragment",
        description="Enable/disable drop fragment packets.",
    )
    drop_overlapped_fragment: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("drop-overlapped-fragment", "drop_overlapped_fragment"),
        serialization_alias="drop-overlapped-fragment",
        description="Enable/disable drop overlapped fragment packets.",
    )
    eap_ca_cert: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("eap-ca-cert", "eap_ca_cert"),
        serialization_alias="eap-ca-cert",
        description="EAP CA certificate name.",
    )
    eap_identity: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("eap-identity", "eap_identity"),
        serialization_alias="eap-identity",
        description="EAP identity.",
    )
    eap_method: Optional[Literal["tls", "peap"]] = Field(
        None,
        validation_alias=AliasChoices("eap-method", "eap_method"),
        serialization_alias="eap-method",
        description="EAP method.",
    )
    eap_password: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("eap-password", "eap_password"),
        serialization_alias="eap-password",
        description="EAP password.",
        repr=False,
    )
    eap_supplicant: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("eap-supplicant", "eap_supplicant"),
        serialization_alias="eap-supplicant",
        description="Enable/disable EAP-Supplicant.",
    )
    eap_user_cert: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("eap-user-cert", "eap_user_cert"),
        serialization_alias="eap-user-cert",
        description="EAP user certificate name.",
    )
    egress_cos: Optional[Literal["disable", "cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]] = Field(
        None,
        validation_alias=AliasChoices("egress-cos", "egress_cos"),
        serialization_alias="egress-cos",
        description="Override outgoing CoS in user VLAN tag.",
    )
    egress_queues: Optional[InterfaceEgressQueues] = Field(
        None, validation_alias=AliasChoices("egress-queues", "egress_queues"), serialization_alias="egress-queues"
    )
    egress_shaping_profile: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("egress-shaping-profile", "egress_shaping_profile"),
        serialization_alias="egress-shaping-profile",
        description="Outgoing traffic shaping profile.",
    )
    eip: Optional[str] = Field(None)
    estimated_downstream_bandwidth: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("estimated-downstream-bandwidth", "estimated_downstream_bandwidth"),
        serialization_alias="estimated-downstream-bandwidth",
        description="Estimated maximum downstream bandwidth (kbps). Used to estimate link utilization.",
    )
    estimated_upstream_bandwidth: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("estimated-upstream-bandwidth", "estimated_upstream_bandwidth"),
        serialization_alias="estimated-upstream-bandwidth",
        description="Estimated maximum upstream bandwidth (kbps). Used to estimate link utilization.",
    )
    explicit_ftp_proxy: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("explicit-ftp-proxy", "explicit_ftp_proxy"),
        serialization_alias="explicit-ftp-proxy",
        description="Enable/disable the explicit FTP proxy on this interface.",
    )
    explicit_web_proxy: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("explicit-web-proxy", "explicit_web_proxy"),
        serialization_alias="explicit-web-proxy",
        description="Enable/disable the explicit web proxy on this interface.",
    )
    external: Optional[Literal["disable", "enable"]] = Field(
        None,
        description=(
            "Enable/disable identifying the interface as an external interface (which usually means it's "
            "connected to the Internet)."
        ),
    )
    fail_action_on_extender: Optional[Literal["soft-restart", "hard-restart", "reboot"]] = Field(
        None,
        validation_alias=AliasChoices("fail-action-on-extender", "fail_action_on_extender"),
        serialization_alias="fail-action-on-extender",
        description="Action on FortiExtender when interface fail.",
    )
    fail_alert_interfaces: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("fail-alert-interfaces", "fail_alert_interfaces"),
        serialization_alias="fail-alert-interfaces",
        description="Names of the FortiGate interfaces to which the link failure alert is sent.",
    )
    fail_alert_method: Optional[Literal["link-failed-signal", "link-down"]] = Field(
        None,
        validation_alias=AliasChoices("fail-alert-method", "fail_alert_method"),
        serialization_alias="fail-alert-method",
        description="Select link-failed-signal or link-down method to alert about a failed link.",
    )
    fail_detect: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("fail-detect", "fail_detect"),
        serialization_alias="fail-detect",
        description="Enable/disable fail detection features for this interface.",
    )
    fail_detect_option: Optional[list[Literal["detectserver", "link-down"]]] = Field(
        None,
        validation_alias=AliasChoices("fail-detect-option", "fail_detect_option"),
        serialization_alias="fail-detect-option",
        description="Options for detecting that this interface has failed.",
    )
    fortilink_backup_link: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("fortilink-backup-link", "fortilink_backup_link"),
        serialization_alias="fortilink-backup-link",
    )
    fortilink_neighbor_detect: Optional[Literal["lldp", "fortilink"]] = Field(
        None,
        validation_alias=AliasChoices("fortilink-neighbor-detect", "fortilink_neighbor_detect"),
        serialization_alias="fortilink-neighbor-detect",
        description="Protocol for FortiGate neighbor discovery.",
    )
    fortilink_split_interface: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("fortilink-split-interface", "fortilink_split_interface"),
        serialization_alias="fortilink-split-interface",
        description=(
            "Enable/disable FortiLink split interface to connect member link to different FortiSwitch in "
            "stack for uplink redundancy."
        ),
    )
    forward_domain: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("forward-domain", "forward_domain"),
        serialization_alias="forward-domain",
        description="Transparent mode forward domain.",
    )
    forward_error_correction: Optional[
        Literal[
            "disable",
            "enable",
            "rs-fec",
            "base-r-fec",
            "rs-544",
            "none",
            "cl91-rs-fec",
            "cl74-fc-fec",
            "auto",
            "rs-fec544",
        ]
    ] = Field(
        None,
        validation_alias=AliasChoices("forward-error-correction", "forward_error_correction"),
        serialization_alias="forward-error-correction",
        description="Enable/disable forward error correction (FEC).",
    )
    gateway_address: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("gateway-address", "gateway_address"),
        serialization_alias="gateway-address",
        description="Gateway address.",
    )
    gi_gk: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("gi-gk", "gi_gk"),
        serialization_alias="gi-gk",
        description="Enable/disable Gi Gatekeeper.",
    )
    ident_accept: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ident-accept", "ident_accept"),
        serialization_alias="ident-accept",
        description="Enable/disable authentication for this interface.",
    )
    idle_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("idle-timeout", "idle_timeout"),
        serialization_alias="idle-timeout",
        description="PPPoE auto disconnect after idle timeout seconds, 0 means no timeout.",
    )
    ike_saml_server: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ike-saml-server", "ike_saml_server"),
        serialization_alias="ike-saml-server",
        description="Configure IKE authentication SAML server.",
    )
    inbandwidth: Optional[int] = Field(
        None, description="Bandwidth limit for incoming traffic (0 - 80000000 kbps), 0 means unlimited."
    )
    ingress_cos: Optional[Literal["disable", "cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]] = Field(
        None,
        validation_alias=AliasChoices("ingress-cos", "ingress_cos"),
        serialization_alias="ingress-cos",
        description=(
            "Override incoming CoS in user VLAN tag on VLAN interface or assign a priority VLAN tag on "
            "physical interface."
        ),
    )
    ingress_shaping_profile: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ingress-shaping-profile", "ingress_shaping_profile"),
        serialization_alias="ingress-shaping-profile",
        description="Incoming traffic shaping profile.",
    )
    ingress_spillover_threshold: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ingress-spillover-threshold", "ingress_spillover_threshold"),
        serialization_alias="ingress-spillover-threshold",
        description="Ingress Spillover threshold (0 - 16776000 kbps), 0 means unlimited.",
    )
    interconnect_profile: Optional[Literal["default", "profile1", "profile2"]] = Field(
        None,
        validation_alias=AliasChoices("interconnect-profile", "interconnect_profile"),
        serialization_alias="interconnect-profile",
        description="Set interconnect profile.",
    )
    internal: Optional[int] = Field(None, description="Implicitly created.")
    ip_managed_by_fortiipam: Optional[Literal["disable", "enable", "inherit-global"]] = Field(
        None,
        validation_alias=AliasChoices("ip-managed-by-fortiipam", "ip_managed_by_fortiipam"),
        serialization_alias="ip-managed-by-fortiipam",
        description="Enable/disable automatic IP address assignment of this interface by FortiIPAM.",
    )
    ips_sniffer_mode: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ips-sniffer-mode", "ips_sniffer_mode"),
        serialization_alias="ips-sniffer-mode",
        description="Enable/disable the use of this interface as a one-armed sniffer.",
    )
    ipunnumbered: Optional[str] = Field(
        None, description="Unnumbered IP used for PPPoE interfaces for which no unique local address is provided."
    )
    ipv6: Optional[InterfaceIpv6] = Field(None)
    l2forward: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable l2 forwarding.")
    l2tp_client: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("l2tp-client", "l2tp_client"),
        serialization_alias="l2tp-client",
        description="Enable/disable this interface as a Layer 2 Tunnelling Protocol (L2TP) client.",
    )
    l2tp_client_settings: Optional[InterfaceL2tpClientSettings] = Field(
        None,
        validation_alias=AliasChoices("l2tp-client-settings", "l2tp_client_settings"),
        serialization_alias="l2tp-client-settings",
    )
    lcp_echo_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("lcp-echo-interval", "lcp_echo_interval"),
        serialization_alias="lcp-echo-interval",
        description="Time in seconds between PPPoE Link Control Protocol (LCP) echo requests.",
    )
    lcp_max_echo_fails: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("lcp-max-echo-fails", "lcp_max_echo_fails"),
        serialization_alias="lcp-max-echo-fails",
        description="Maximum missed LCP echo messages before disconnect.",
    )
    link_up_delay: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("link-up-delay", "link_up_delay"),
        serialization_alias="link-up-delay",
        description="Number of milliseconds to wait before considering a link is up.",
    )
    managed_subnetwork_size: Optional[
        Literal["32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32768", "65536"]
    ] = Field(
        None,
        validation_alias=AliasChoices("managed-subnetwork-size", "managed_subnetwork_size"),
        serialization_alias="managed-subnetwork-size",
        description=(
            "Number of IP addresses to be allocated by FortiIPAM and used by this FortiGate unit's DHCP "
            "server settings."
        ),
    )
    measured_downstream_bandwidth: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("measured-downstream-bandwidth", "measured_downstream_bandwidth"),
        serialization_alias="measured-downstream-bandwidth",
        description="Measured downstream bandwidth (kbps).",
    )
    measured_upstream_bandwidth: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("measured-upstream-bandwidth", "measured_upstream_bandwidth"),
        serialization_alias="measured-upstream-bandwidth",
        description="Measured upstream bandwidth (kbps).",
    )
    mediatype: Optional[
        Literal[
            "serdes-sfp",
            "sgmii-sfp",
            "serdes-copper-sfp",
            "sr",
            "cr",
            "lr",
            "qsfp28-sr4",
            "qsfp28-lr4",
            "qsfp28-cr4",
            "sr4",
            "cr4",
            "lr4",
            "none",
            "gmii",
            "sgmii",
            "sr2",
            "lr2",
            "cr2",
            "sr8",
            "lr8",
            "cr8",
            "sr-lr",
            "kr",
        ]
    ] = Field(None, description="Select SFP media interface type")
    min_links: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("min-links", "min_links"),
        serialization_alias="min-links",
        description="Minimum number of aggregated ports that must be up.",
    )
    min_links_down: Optional[Literal["operational", "administrative"]] = Field(
        None,
        validation_alias=AliasChoices("min-links-down", "min_links_down"),
        serialization_alias="min-links-down",
        description="Action to take when less than the configured minimum number of links are active.",
    )
    mirroring_direction: Optional[Literal["rx", "tx", "both"]] = Field(
        None,
        validation_alias=AliasChoices("mirroring-direction", "mirroring_direction"),
        serialization_alias="mirroring-direction",
        description="Port mirroring direction.",
    )
    mirroring_filter: Optional[InterfaceMirroringFilter] = Field(
        None,
        validation_alias=AliasChoices("mirroring-filter", "mirroring_filter"),
        serialization_alias="mirroring-filter",
    )
    mirroring_port: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("mirroring-port", "mirroring_port"),
        serialization_alias="mirroring-port",
        description="Mirroring port.",
    )
    monitor_bandwidth: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("monitor-bandwidth", "monitor_bandwidth"),
        serialization_alias="monitor-bandwidth",
        description="Enable monitoring bandwidth on this interface.",
    )
    mux_type: Optional[Literal["llc-encaps", "vc-encaps"]] = Field(
        None,
        validation_alias=AliasChoices("mux-type", "mux_type"),
        serialization_alias="mux-type",
        description="Multiplexer type.",
    )
    ndiscforward: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable NDISC forwarding.")
    netbios_forward: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("netbios-forward", "netbios_forward"),
        serialization_alias="netbios-forward",
        description="Enable/disable NETBIOS forwarding.",
    )
    netflow_sampler: Optional[Literal["disable", "tx", "rx", "both"]] = Field(
        None,
        validation_alias=AliasChoices("netflow-sampler", "netflow_sampler"),
        serialization_alias="netflow-sampler",
        description=(
            "Enable/disable NetFlow on this interface and set the data that NetFlow collects (rx, tx, or both)."
        ),
    )
    np_qos_profile: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("np-qos-profile", "np_qos_profile"),
        serialization_alias="np-qos-profile",
        description="NP QoS profile ID.",
    )
    outbandwidth: Optional[int] = Field(None, description="Bandwidth limit for outgoing traffic (0 - 80000000 kbps).")
    padt_retry_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("padt-retry-timeout", "padt_retry_timeout"),
        serialization_alias="padt-retry-timeout",
        description="PPPoE Active Discovery Terminate (PADT) used to terminate sessions after an idle time.",
    )
    password: Optional[list[str]] = Field(None, description="PPPoE account's password.", repr=False)
    phy_mode: Optional[
        Literal["auto", "adsl", "vdsl", "adsl-auto", "vdsl2", "adsl2+", "adsl2", "g-dmt", "t1-413", "g-lite"]
    ] = Field(
        None,
        validation_alias=AliasChoices("phy-mode", "phy_mode"),
        serialization_alias="phy-mode",
        description="DSL physical mode.",
    )
    phy_setting: Optional[InterfacePhySetting] = Field(
        None, validation_alias=AliasChoices("phy-setting", "phy_setting"), serialization_alias="phy-setting"
    )
    poe: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable PoE status.")
    polling_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("polling-interval", "polling_interval"),
        serialization_alias="polling-interval",
        description="sFlow polling interval in seconds (1 - 255).",
    )
    port_mirroring: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("port-mirroring", "port_mirroring"),
        serialization_alias="port-mirroring",
        description="Enable/disable NP port mirroring.",
    )
    pppoe_egress_cos: Optional[Literal["cos0", "cos1", "cos2", "cos3", "cos4", "cos5", "cos6", "cos7"]] = Field(
        None,
        validation_alias=AliasChoices("pppoe-egress-cos", "pppoe_egress_cos"),
        serialization_alias="pppoe-egress-cos",
        description="CoS in VLAN tag for outgoing PPPoE/PPP packets.",
    )
    pppoe_unnumbered_negotiate: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("pppoe-unnumbered-negotiate", "pppoe_unnumbered_negotiate"),
        serialization_alias="pppoe-unnumbered-negotiate",
        description="Enable/disable PPPoE unnumbered negotiation.",
    )
    pptp_auth_type: Optional[Literal["auto", "pap", "chap", "mschapv1", "mschapv2"]] = Field(
        None,
        validation_alias=AliasChoices("pptp-auth-type", "pptp_auth_type"),
        serialization_alias="pptp-auth-type",
        description="PPTP authentication type.",
    )
    pptp_client: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("pptp-client", "pptp_client"),
        serialization_alias="pptp-client",
        description="Enable/disable PPTP client.",
    )
    pptp_password: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("pptp-password", "pptp_password"),
        serialization_alias="pptp-password",
        description="PPTP password.",
        repr=False,
    )
    pptp_server_ip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("pptp-server-ip", "pptp_server_ip"),
        serialization_alias="pptp-server-ip",
        description="PPTP server IP address.",
    )
    pptp_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pptp-timeout", "pptp_timeout"),
        serialization_alias="pptp-timeout",
        description="Idle timer in minutes (0 for disabled).",
    )
    pptp_user: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("pptp-user", "pptp_user"),
        serialization_alias="pptp-user",
        description="PPTP user name.",
    )
    preserve_session_route: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("preserve-session-route", "preserve_session_route"),
        serialization_alias="preserve-session-route",
        description="Enable/disable preservation of session route when dirty.",
    )
    priority: Optional[int] = Field(None, description="Priority of learned routes.")
    priority_override: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("priority-override", "priority_override"),
        serialization_alias="priority-override",
        description="Enable/disable fail back to higher priority port once recovered.",
    )
    profiles: Optional[list[Literal["8a", "8b", "8c", "8d", "12a", "12b", "17a", "30a", "35b"]]] = Field(
        None, description="Set allowed VDSL profiles."
    )
    proxy_captive_portal: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("proxy-captive-portal", "proxy_captive_portal"),
        serialization_alias="proxy-captive-portal",
        description="Enable/disable proxy captive portal on this interface.",
    )
    pvc_atm_qos: Optional[Literal["cbr", "rt-vbr", "nrt-vbr", "ubr"]] = Field(
        None,
        validation_alias=AliasChoices("pvc-atm-qos", "pvc_atm_qos"),
        serialization_alias="pvc-atm-qos",
        description="SFP-DSL ADSL Fallback PVC ATM QoS.",
    )
    pvc_chan: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pvc-chan", "pvc_chan"),
        serialization_alias="pvc-chan",
        description="SFP-DSL ADSL Fallback PVC Channel.",
    )
    pvc_crc: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pvc-crc", "pvc_crc"),
        serialization_alias="pvc-crc",
        description=(
            "SFP-DSL ADSL Fallback PVC CRC Option:  bit0: sar LLC preserve, bit1: ream LLC preserve, bit2: "
            "ream VC-MUX has crc."
        ),
    )
    pvc_pcr: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pvc-pcr", "pvc_pcr"),
        serialization_alias="pvc-pcr",
        description="SFP-DSL ADSL Fallback PVC Packet Cell Rate in cells (0 - 5500).",
    )
    pvc_scr: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pvc-scr", "pvc_scr"),
        serialization_alias="pvc-scr",
        description="SFP-DSL ADSL Fallback PVC Sustainable Cell Rate in cells (0 - 5500).",
    )
    pvc_vlan_id: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pvc-vlan-id", "pvc_vlan_id"),
        serialization_alias="pvc-vlan-id",
        description="SFP-DSL ADSL Fallback PVC VLAN ID.",
    )
    pvc_vlan_rx_id: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pvc-vlan-rx-id", "pvc_vlan_rx_id"),
        serialization_alias="pvc-vlan-rx-id",
        description="SFP-DSL ADSL Fallback PVC VLANID RX.",
    )
    pvc_vlan_rx_op: Optional[Literal["pass-through", "replace", "remove"]] = Field(
        None,
        validation_alias=AliasChoices("pvc-vlan-rx-op", "pvc_vlan_rx_op"),
        serialization_alias="pvc-vlan-rx-op",
        description="SFP-DSL ADSL Fallback PVC VLAN RX op.",
    )
    pvc_vlan_tx_id: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("pvc-vlan-tx-id", "pvc_vlan_tx_id"),
        serialization_alias="pvc-vlan-tx-id",
        description="SFP-DSL ADSL Fallback PVC VLAN ID TX.",
    )
    pvc_vlan_tx_op: Optional[Literal["pass-through", "replace", "remove"]] = Field(
        None,
        validation_alias=AliasChoices("pvc-vlan-tx-op", "pvc_vlan_tx_op"),
        serialization_alias="pvc-vlan-tx-op",
        description="SFP-DSL ADSL Fallback PVC VLAN TX op.",
    )
    reachable_time: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("reachable-time", "reachable_time"),
        serialization_alias="reachable-time",
        description="IPv4 reachable time in milliseconds (30000 - 3600000, default = 30000).",
    )
    redundant_interface: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("redundant-interface", "redundant_interface"),
        serialization_alias="redundant-interface",
    )
    remote_ip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("remote-ip", "remote_ip"),
        serialization_alias="remote-ip",
        description="Remote IP address of tunnel.",
    )
    replacemsg_override_group: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("replacemsg-override-group", "replacemsg_override_group"),
        serialization_alias="replacemsg-override-group",
        description="Replacement message override group.",
    )
    retransmission: Optional[Literal["disable", "enable"]] = Field(
        None, description="Enable/disable DSL retransmission."
    )
    ring_rx: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ring-rx", "ring_rx"),
        serialization_alias="ring-rx",
        description="RX ring size.",
    )
    ring_tx: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ring-tx", "ring_tx"),
        serialization_alias="ring-tx",
        description="TX ring size.",
    )
    sample_direction: Optional[Literal["rx", "tx", "both"]] = Field(
        None,
        validation_alias=AliasChoices("sample-direction", "sample_direction"),
        serialization_alias="sample-direction",
        description="Data that NetFlow collects (rx, tx, or both).",
    )
    sample_rate: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("sample-rate", "sample_rate"),
        serialization_alias="sample-rate",
        description="sFlow sample rate (10 - 99999).",
    )
    security_8021x_dynamic_vlan_id: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("security-8021x-dynamic-vlan-id", "security_8021x_dynamic_vlan_id"),
        serialization_alias="security-8021x-dynamic-vlan-id",
        description="VLAN ID for virtual switch.",
    )
    security_8021x_master: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("security-8021x-master", "security_8021x_master"),
        serialization_alias="security-8021x-master",
        description="802.1X master virtual-switch.",
    )
    security_8021x_member_mode: Optional[Literal["disable", "switch"]] = Field(
        None,
        validation_alias=AliasChoices("security-8021x-member-mode", "security_8021x_member_mode"),
        serialization_alias="security-8021x-member-mode",
        description="802.1X member mode.",
    )
    security_8021x_mode: Optional[Literal["default", "dynamic-vlan", "fallback", "slave"]] = Field(
        None,
        validation_alias=AliasChoices("security-8021x-mode", "security_8021x_mode"),
        serialization_alias="security-8021x-mode",
        description="802.1X mode.",
    )
    security_exempt_list: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("security-exempt-list", "security_exempt_list"),
        serialization_alias="security-exempt-list",
        description="Name of security-exempt-list.",
    )
    security_external_logout: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("security-external-logout", "security_external_logout"),
        serialization_alias="security-external-logout",
        description="URL of external authentication logout server.",
    )
    security_external_web: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("security-external-web", "security_external_web"),
        serialization_alias="security-external-web",
        description="URL of external authentication web server.",
    )
    security_groups: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("security-groups", "security_groups"),
        serialization_alias="security-groups",
        description="User groups that can authenticate with the captive portal.",
    )
    security_mac_auth_bypass: Optional[Literal["disable", "enable", "mac-auth-only"]] = Field(
        None,
        validation_alias=AliasChoices("security-mac-auth-bypass", "security_mac_auth_bypass"),
        serialization_alias="security-mac-auth-bypass",
        description="Enable/disable MAC authentication bypass.",
    )
    security_mode: Optional[Literal["none", "captive-portal", "802.1X"]] = Field(
        None,
        validation_alias=AliasChoices("security-mode", "security_mode"),
        serialization_alias="security-mode",
        description="Turn on captive portal authentication for this interface.",
    )
    security_redirect_url: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("security-redirect-url", "security_redirect_url"),
        serialization_alias="security-redirect-url",
        description="URL redirection after disclaimer/authentication.",
    )
    select_profile_30a_35b: Optional[Literal["30A", "30a", "35B", "35b"]] = Field(
        None,
        validation_alias=AliasChoices("select-profile-30a-35b", "select_profile_30a_35b"),
        serialization_alias="select-profile-30a-35b",
        description="Select VDSL Profile 30a or 35b.",
    )
    service_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("service-name", "service_name"),
        serialization_alias="service-name",
        description="PPPoE service name.",
    )
    sflow_sampler: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("sflow-sampler", "sflow_sampler"),
        serialization_alias="sflow-sampler",
        description="Enable/disable sFlow on this interface.",
    )
    sfp_dsl: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("sfp-dsl", "sfp_dsl"),
        serialization_alias="sfp-dsl",
        description="Enable/disable SFP DSL.",
    )
    sfp_dsl_adsl_fallback: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("sfp-dsl-adsl-fallback", "sfp_dsl_adsl_fallback"),
        serialization_alias="sfp-dsl-adsl-fallback",
        description="Enable/disable SFP DSL ADSL fallback.",
    )
    sfp_dsl_autodetect: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("sfp-dsl-autodetect", "sfp_dsl_autodetect"),
        serialization_alias="sfp-dsl-autodetect",
        description="Enable/disable SFP DSL MAC address autodetect.",
    )
    sfp_dsl_mac: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("sfp-dsl-mac", "sfp_dsl_mac"),
        serialization_alias="sfp-dsl-mac",
        description="SFP DSL MAC address.",
    )
    snmp_index: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("snmp-index", "snmp_index"),
        serialization_alias="snmp-index",
        description="Permanent SNMP Index of the interface.",
    )
    spillover_threshold: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("spillover-threshold", "spillover_threshold"),
        serialization_alias="spillover-threshold",
        description="Egress Spillover threshold (0 - 16776000 kbps), 0 means unlimited.",
    )
    stp: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable STP.")
    stp_edge: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("stp-edge", "stp_edge"),
        serialization_alias="stp-edge",
        description="Enable/disable as STP edge port.",
    )
    stp_ha_secondary: Optional[Literal["disable", "enable", "priority-adjust"]] = Field(
        None,
        validation_alias=AliasChoices("stp-ha-secondary", "stp_ha_secondary"),
        serialization_alias="stp-ha-secondary",
        description="Control STP behavior on HA secondary.",
    )
    subst: Optional[Literal["disable", "enable"]] = Field(
        None, description="Enable to always send packets from this interface to a destination MAC address."
    )
    substitute_dst_mac: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("substitute-dst-mac", "substitute_dst_mac"),
        serialization_alias="substitute-dst-mac",
        description="Destination MAC address that all packets are sent to from this interface.",
    )
    sw_algorithm: Optional[Literal["l2", "l3", "eh", "default"]] = Field(
        None,
        validation_alias=AliasChoices("sw-algorithm", "sw_algorithm"),
        serialization_alias="sw-algorithm",
        description="Frame distribution algorithm for switch.",
    )
    swc_first_create: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("swc-first-create", "swc_first_create"),
        serialization_alias="swc-first-create",
        description="Initial create for switch-controller VLANs.",
    )
    swc_vlan: Optional[int] = Field(
        None, validation_alias=AliasChoices("swc-vlan", "swc_vlan"), serialization_alias="swc-vlan"
    )
    switch: Optional[str] = Field(None)
    switch_controller_access_vlan: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-access-vlan", "switch_controller_access_vlan"),
        serialization_alias="switch-controller-access-vlan",
        description="Block FortiSwitch port-to-port traffic.",
    )
    switch_controller_arp_inspection: Optional[Literal["disable", "enable", "monitor"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-arp-inspection", "switch_controller_arp_inspection"),
        serialization_alias="switch-controller-arp-inspection",
        description="Enable/disable/Monitor FortiSwitch ARP inspection.",
    )
    switch_controller_dhcp_snooping: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-dhcp-snooping", "switch_controller_dhcp_snooping"),
        serialization_alias="switch-controller-dhcp-snooping",
        description="Switch controller DHCP snooping.",
    )
    switch_controller_dhcp_snooping_option82: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices(
            "switch-controller-dhcp-snooping-option82", "switch_controller_dhcp_snooping_option82"
        ),
        serialization_alias="switch-controller-dhcp-snooping-option82",
        description="Switch controller DHCP snooping option82.",
    )
    switch_controller_dhcp_snooping_verify_mac: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices(
            "switch-controller-dhcp-snooping-verify-mac", "switch_controller_dhcp_snooping_verify_mac"
        ),
        serialization_alias="switch-controller-dhcp-snooping-verify-mac",
        description="Switch controller DHCP snooping verify MAC.",
    )
    switch_controller_dynamic: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-dynamic", "switch_controller_dynamic"),
        serialization_alias="switch-controller-dynamic",
        description="Integrated FortiLink settings for managed FortiSwitch.",
    )
    switch_controller_feature: Optional[
        Literal["none", "default-vlan", "quarantine", "voice", "rspan", "video", "nac", "nac-segment"]
    ] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-feature", "switch_controller_feature"),
        serialization_alias="switch-controller-feature",
        description="Interface's purpose when assigning traffic (read only).",
    )
    switch_controller_igmp_snooping: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-igmp-snooping", "switch_controller_igmp_snooping"),
        serialization_alias="switch-controller-igmp-snooping",
        description="Switch controller IGMP snooping.",
    )
    switch_controller_igmp_snooping_fast_leave: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices(
            "switch-controller-igmp-snooping-fast-leave", "switch_controller_igmp_snooping_fast_leave"
        ),
        serialization_alias="switch-controller-igmp-snooping-fast-leave",
        description="Switch controller IGMP snooping fast-leave.",
    )
    switch_controller_igmp_snooping_proxy: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-igmp-snooping-proxy", "switch_controller_igmp_snooping_proxy"),
        serialization_alias="switch-controller-igmp-snooping-proxy",
        description="Switch controller IGMP snooping proxy.",
    )
    switch_controller_iot_scanning: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-iot-scanning", "switch_controller_iot_scanning"),
        serialization_alias="switch-controller-iot-scanning",
        description="Enable/disable managed FortiSwitch IoT scanning.",
    )
    switch_controller_learning_limit: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-learning-limit", "switch_controller_learning_limit"),
        serialization_alias="switch-controller-learning-limit",
        description="Limit the number of dynamic MAC addresses on this VLAN (1 - 128, 0 = no limit, default).",
    )
    switch_controller_mgmt_vlan: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-mgmt-vlan", "switch_controller_mgmt_vlan"),
        serialization_alias="switch-controller-mgmt-vlan",
        description="VLAN to use for FortiLink management purposes.",
    )
    switch_controller_nac: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-nac", "switch_controller_nac"),
        serialization_alias="switch-controller-nac",
        description="Integrated FortiLink settings for managed FortiSwitch.",
    )
    switch_controller_netflow_collect: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-netflow-collect", "switch_controller_netflow_collect"),
        serialization_alias="switch-controller-netflow-collect",
        description="NetFlow collection and processing.",
    )
    switch_controller_offload: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-offload", "switch_controller_offload"),
        serialization_alias="switch-controller-offload",
        description="Enable/disable managed FortiSwitch routing offload.",
    )
    switch_controller_offload_gw: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-offload-gw", "switch_controller_offload_gw"),
        serialization_alias="switch-controller-offload-gw",
        description="Enable/disable managed FortiSwitch routing offload gateway.",
    )
    switch_controller_offload_ip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-offload-ip", "switch_controller_offload_ip"),
        serialization_alias="switch-controller-offload-ip",
        description="IP for routing offload on FortiSwitch.",
    )
    switch_controller_rspan_mode: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-rspan-mode", "switch_controller_rspan_mode"),
        serialization_alias="switch-controller-rspan-mode",
        description="Stop Layer2 MAC learning and interception of BPDUs and other packets on this interface.",
    )
    switch_controller_source_ip: Optional[Literal["outbound", "fixed"]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-source-ip", "switch_controller_source_ip"),
        serialization_alias="switch-controller-source-ip",
        description="Source IP address used in FortiLink over L3 connections.",
    )
    switch_controller_traffic_policy: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("switch-controller-traffic-policy", "switch_controller_traffic_policy"),
        serialization_alias="switch-controller-traffic-policy",
        description="Switch controller traffic policy for the VLAN.",
    )
    system_id: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("system-id", "system_id"),
        serialization_alias="system-id",
        description="Define a system ID for the aggregate interface.",
    )
    system_id_type: Optional[Literal["auto", "user"]] = Field(
        None,
        validation_alias=AliasChoices("system-id-type", "system_id_type"),
        serialization_alias="system-id-type",
        description="Method in which system ID is generated.",
    )
    tagging: Optional[list[InterfaceTagging]] = Field(None)
    tc_mode: Optional[Literal["ptm", "atm"]] = Field(
        None,
        validation_alias=AliasChoices("tc-mode", "tc_mode"),
        serialization_alias="tc-mode",
        description="DSL transfer mode.",
    )
    trunk: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable VLAN trunk.")
    trust_ip_1: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("trust-ip-1", "trust_ip_1"),
        serialization_alias="trust-ip-1",
        description="Trusted host for dedicated management traffic (0.0.0.0/24 for all hosts).",
    )
    trust_ip_2: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("trust-ip-2", "trust_ip_2"),
        serialization_alias="trust-ip-2",
        description="Trusted host for dedicated management traffic (0.0.0.0/24 for all hosts).",
    )
    trust_ip_3: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("trust-ip-3", "trust_ip_3"),
        serialization_alias="trust-ip-3",
        description="Trusted host for dedicated management traffic (0.0.0.0/24 for all hosts).",
    )
    trust_ip6_1: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("trust-ip6-1", "trust_ip6_1"),
        serialization_alias="trust-ip6-1",
        description="Trusted IPv6 host for dedicated management traffic (::/0 for all hosts).",
    )
    trust_ip6_2: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("trust-ip6-2", "trust_ip6_2"),
        serialization_alias="trust-ip6-2",
        description="Trusted IPv6 host for dedicated management traffic (::/0 for all hosts).",
    )
    trust_ip6_3: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("trust-ip6-3", "trust_ip6_3"),
        serialization_alias="trust-ip6-3",
        description="Trusted IPv6 host for dedicated management traffic (::/0 for all hosts).",
    )
    username: Optional[str] = Field(None, description="Username of the PPPoE account, provided by your ISP.")
    vci: Optional[int] = Field(None, description="Virtual Channel ID.")
    vectoring: Optional[Literal["disable", "enable"]] = Field(None, description="Enable/disable DSL vectoring.")
    vlan_id: Optional[int] = Field(
        None, validation_alias=AliasChoices("vlan-id", "vlan_id"), serialization_alias="vlan-id", description="Vlan ID."
    )
    vlan_op_mode: Optional[Literal["tag", "untag", "passthrough"]] = Field(
        None,
        validation_alias=AliasChoices("vlan-op-mode", "vlan_op_mode"),
        serialization_alias="vlan-op-mode",
        description="Configure DSL 802.1q mode.",
    )
    vlanforward: Optional[Literal["disable", "enable"]] = Field(
        None, description="Enable/disable traffic forwarding between VLANs on this interface."
    )
    vpi: Optional[int] = Field(None, description="Virtual Path ID.")
    wccp: Optional[Literal["disable", "enable"]] = Field(
        None,
        description=(
            "Enable/disable WCCP on this interface. Used for encapsulated WCCP communication between WCCP "
            "clients and servers."
        ),
    )
    wifi_5g_threshold: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-5g-threshold", "wifi_5g_threshold"),
        serialization_alias="wifi-5g-threshold",
        description="Minimal signal strength to be considered as a good 5G AP.",
    )
    wifi_acl: Optional[Literal["deny", "allow"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-acl", "wifi_acl"),
        serialization_alias="wifi-acl",
        description="Access control for MAC addresses in the MAC list.",
    )
    wifi_ap_band: Optional[Literal["any", "5g-preferred", "5g-only"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-ap-band", "wifi_ap_band"),
        serialization_alias="wifi-ap-band",
        description="How to select the AP to connect.",
    )
    wifi_auth: Optional[Literal["PSK", "radius", "usergroup"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-auth", "wifi_auth"),
        serialization_alias="wifi-auth",
        description="WiFi authentication.",
    )
    wifi_auto_connect: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-auto-connect", "wifi_auto_connect"),
        serialization_alias="wifi-auto-connect",
        description="Enable/disable WiFi network auto connect.",
    )
    wifi_auto_save: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-auto-save", "wifi_auto_save"),
        serialization_alias="wifi-auto-save",
        description="Enable/disable WiFi network automatic save.",
    )
    wifi_broadcast_ssid: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-broadcast-ssid", "wifi_broadcast_ssid"),
        serialization_alias="wifi-broadcast-ssid",
        description="Enable/disable SSID broadcast in the beacon.",
    )
    wifi_dns_server1: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-dns-server1", "wifi_dns_server1"),
        serialization_alias="wifi-dns-server1",
        description="DNS server 1.",
    )
    wifi_dns_server2: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-dns-server2", "wifi_dns_server2"),
        serialization_alias="wifi-dns-server2",
        description="DNS server 2.",
    )
    wifi_encrypt: Optional[Literal["TKIP", "AES"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-encrypt", "wifi_encrypt"),
        serialization_alias="wifi-encrypt",
        description="Data encryption.",
    )
    wifi_fragment_threshold: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("wifi-fragment-threshold", "wifi_fragment_threshold"),
        serialization_alias="wifi-fragment-threshold",
        description="WiFi fragment threshold (800 - 2346).",
    )
    wifi_gateway: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-gateway", "wifi_gateway"),
        serialization_alias="wifi-gateway",
        description="IPv4 default gateway IP address.",
    )
    wifi_key: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("wifi-key", "wifi_key"),
        serialization_alias="wifi-key",
        description="WiFi WEP Key.",
    )
    wifi_keyindex: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("wifi-keyindex", "wifi_keyindex"),
        serialization_alias="wifi-keyindex",
        description="WEP key index (1 - 4).",
    )
    wifi_mac_filter: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("wifi-mac-filter", "wifi_mac_filter"),
        serialization_alias="wifi-mac-filter",
        description="Enable/disable MAC filter status.",
    )
    wifi_networks: Optional[list[InterfaceWifiNetworks]] = Field(
        None, validation_alias=AliasChoices("wifi-networks", "wifi_networks"), serialization_alias="wifi-networks"
    )
    wifi_passphrase: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("wifi-passphrase", "wifi_passphrase"),
        serialization_alias="wifi-passphrase",
        description="WiFi pre-shared key for WPA.",
    )
    wifi_radius_server: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("wifi-radius-server", "wifi_radius_server"),
        serialization_alias="wifi-radius-server",
        description="WiFi RADIUS server for WPA.",
    )
    wifi_rts_threshold: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("wifi-rts-threshold", "wifi_rts_threshold"),
        serialization_alias="wifi-rts-threshold",
        description="WiFi RTS threshold (256 - 2346).",
    )
    wifi_security: Optional[
        Literal[
            "wep64",
            "wep128",
            "open",
            "wpa-personal",
            "wpa-enterprise",
            "wpa-only-personal",
            "wpa-only-enterprise",
            "wpa2-only-personal",
            "wpa2-only-enterprise",
        ]
    ] = Field(
        None,
        validation_alias=AliasChoices("wifi-security", "wifi_security"),
        serialization_alias="wifi-security",
        description="Wireless access security of SSID.",
    )
    wifi_ssid: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-ssid", "wifi_ssid"),
        serialization_alias="wifi-ssid",
        description="IEEE 802.11 Service Set Identifier.",
    )
    wifi_usergroup: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wifi-usergroup", "wifi_usergroup"),
        serialization_alias="wifi-usergroup",
        description="WiFi user group for WPA.",
    )
    wins_ip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("wins-ip", "wins_ip"),
        serialization_alias="wins-ip",
        description="WINS server IP.",
    )
