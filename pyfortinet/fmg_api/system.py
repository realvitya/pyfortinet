"""System objects"""
from ipaddress import IPv4Interface
from typing import Literal, Optional, List, Dict, Union

from pydantic import Field, field_validator, AliasChoices, BaseModel

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.dvmdb import VDOM, Device

ALLOW_ACCESS_TYPE = Literal["https", "ping", "ssh", "snmp", "http", "telnet", "fgfm", "auto-ipsec", "radius-acct", "probe-response", "capwap", "dnp", "ftm", "fabric", "speed-test"]
ENABLE_DISABLE = Literal["disable", "enable"]
INTERFACE_BFD_TYPE = Literal["global", "enable", "disable"]
INTERFACE_MODE_TYPE = Literal["static", "dhcp", "pppoe", "pppoa", "ipoa", "eoa"]
INTERFACE_SPEED_TYPE = Literal["auto", "10full", "10half", "100full", "100half", "1000full", "1000half", "10000full", "1000auto", "10000auto", "40000full", "100Gfull", "25000full", "50000full", "40000auto", "25000auto", "100Gauto", "2500auto", "400Gfull", "400Gauto", "5000auto", "50000auto", "200Gfull", "200Gauto", "100auto"]
INTERFACE_STATUS_TYPE = Literal["down", "up"]
INTERFACE_STPFORWARD_MODE_TYPE = Literal["rpl-all-ext-id", "rpl-bridge-ext-id", "rpl-nothing"]
INTERFACE_ROLE_TYPE = Literal["lan", "wan", "dmz", "undefined"]
INTERFACE_TYPE_TYPE = Literal["physical", "vlan", "aggregate", "redundant", "tunnel", "wireless", "vdom-link", "loopback", "switch", "hard-switch", "hdlc", "vap-switch", "wl-mesh", "fortilink", "switch-vlan", "fctrl-trunk", "tdm", "fext-wan", "vxlan", "emac-vlan", "geneve", "ssl", "lan-extension"]
INTERFACE_VLAN_PROTO_TYPE = Literal["8021q", "8021ad"]
LACP_MODE_TYPE = Literal["static", "passive", "active"]
LACP_SPEED_TYPE = Literal["slow", "fast"]
LLDP_MODE_TYPE = Literal["disable", "enable", "vdom"]
PERMIT_DENY = Literal["deny", "allow"]


class DeviceInterface(FMGObject):
    """Interface object

    Attributes:
        ac_name: PPPoE server name
        aggregate:
        aggregate_type: Type of aggregation
        algorithm: Frame distribution algorithm
        alias: Alias will be displayed with the interface name to make it easier to distinguish
        allowaccess: Permitted types of management access to this interface
        annex:
        ap_discover: Enable/disable automatic registration of unknown FortiAP devices
        arpforward: Enable/disable ARP forwarding
        atm_protocol: ATM protocol
        auth_cert: HTTPS server certificate
        auth_portal_addr: Address of captive portal.
        auth_type: PPP authentication type to use
        auto_auth_extension_device:
            Enable/disable automatic authorization of dedicated Fortinet extension device on this interface.
        bandwidth_measure_time: Bandwidth measure time
        bfd: Bidirectional Forwarding Detection (BFD) settings
        bfd_desired_min_tx: BFD desired minimal transmit interval
        bfd_detect_mult: BFD detection multiplier
        bfd_required_min_rx: BFD required minimal receive interval
        broadcast_forticlient_discovery:
        broadcast_forward: Enable/disable broadcast forwarding

        interface: Specify interface for operation (URL var)
        color:
    """
    _url = "/pm/config/device/{device}/global/system/interface/{fmg_interface}"
    _master_keys = ["name"]
    # URL fields
    device: Optional[str] = Field(None, exclude=True)
    fmg_interface: Optional[str] = Field(None, exclude=True)
    # API fields
    # ac_name
    # aggregate
    # aggregate_type: Optional[str] = Field(None, exclude=True)
    # algorithm
    alias: Optional[str] = None
    allowaccess: Optional[Union[ALLOW_ACCESS_TYPE, List[ALLOW_ACCESS_TYPE]]] = None
    # annex
    # 'ap-discover',
    arpforward: Optional[ENABLE_DISABLE] = None
    # atm_protocol
    # 'auth-cert',
    # auth_portal_addr
    # auth_type
    # 'auto-auth-extension-device',
    # 'bandwidth-measure-time',
    bfd: Optional[INTERFACE_BFD_TYPE] = None
    # bfd_desired_min_tx
    # bfd_detect_mult
    # bfd_required_min_rx
    # broadcast_forticlient_discovery
    broadcast_forward: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("broadcast-forward", "broadcast_forward"),
        serialization_alias="broadcast-forward"
    )
    # 'captive-portal',
    # 'cli-conn-status',
    # 'client-options',
    # 'color',
    # 'dedicated-to',
    # 'detected-peer-mtu',
    # 'device-identification',
    devindex: Optional[int] = None
    # 'dhcp-classless-route-addition',
    # 'dhcp-relay-interface',
    # 'dhcp-relay-interface-select-method',
    # 'dhcp-relay-link-selection',
    # 'dhcp-relay-request-all-server',
    # 'dhcp-relay-service',
    # 'dhcp-renew-time',
    # 'dhcp-snooping-server-list',
    # 'disconnect-threshold',
    # 'dns-server-protocol',
    # 'drop-fragment',
    # 'drop-overlapped-fragment',
    # 'eap-ca-cert',
    # 'eap-password',
    # 'eap-supplicant',
    # 'eap-user-cert',
    # 'egress-queues',
    # 'egress-shaping-profile',
    # 'estimated-downstream-bandwidth',
    # 'estimated-upstream-bandwidth',
    # 'explicit-ftp-proxy',
    # 'explicit-web-proxy',
    # 'external',
    # 'fail-action-on-extender',
    # 'fail-detect',
    fortilink: Optional[ENABLE_DISABLE] = None
    # 'fortilink-backup-link',
    # 'fortilink-neighbor-detect',
    # 'forward-domain',
    icmp_accept_redirect: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("icmp-accept-redirect", "icmp_accept_redirect"),
        serialization_alias="icmp-accept-redirect"
    )
    icmp_send_redirect: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("icmp-send-redirect", "icmp_send_redirect"),
        serialization_alias="icmp-send-redirect"
    )

    # 'ident-accept',
    # 'ike-saml-server',
    # 'inbandwidth',
    # 'ingress-shaping-profile',
    # 'ingress-spillover-threshold',
    interface: Optional[Union["DeviceInterface", List["DeviceInterface"], Union[str, List[str]]]] = None
    # 'internal',
    ip: Optional[Union[str, list]] = None
    # 'ip-managed-by-fortiipam',
    ipmac: Optional[ENABLE_DISABLE] = None
    # 'ips-sniffer-mode',
    # 'ipv6',
    # 'l2forward',
    # 'l2tp-client-settings',
    lacp_ha_secondary: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("lacp-ha-secondary", "lacp_ha_secondary"),
        serialization_alias="lacp-ha-secondary"
    )
    lacp_mode: Optional[LACP_MODE_TYPE] = Field(
        None,
        validation_alias=AliasChoices("lacp-mode", "lacp_mode"),
        serialization_alias="lacp-mode"
    )
    lacp_speed: Optional[LACP_SPEED_TYPE] = Field(
        None,
        validation_alias=AliasChoices("lacp-speed", "lacp_speed"),
        serialization_alias="lacp-speed"
    )
    lldp_network_policy: Optional[Union[str, List[str]]] = Field(
        None,
        validation_alias=AliasChoices("lldp-network-policy", "lldp_network_policy"),
        serialization_alias="lldp-network-policy"
    )
    lldp_reception: Optional[LLDP_MODE_TYPE] = Field(
        None,
        validation_alias=AliasChoices("lldp-reception", "lldp_reception"),
        serialization_alias="lldp-reception"
    )
    lldp_transmission: Optional[LLDP_MODE_TYPE] = Field(
        None,
        validation_alias=AliasChoices("lldp-transmission", "lldp_transmission"),
        serialization_alias="lldp-transmission"
    )
    macaddr: Optional[str] = None
    # 'managed-subnetwork-size',
    management_ip: Optional[Union[str, list]] = Field(
        None,
        validation_alias=AliasChoices("management-ip", "management_ip"),
        serialization_alias="management-ip"
    )
    # 'measured-downstream-bandwidth',
    # 'measured-upstream-bandwidth',
    # 'min-links',
    # 'min-links-down',
    mode: Optional[INTERFACE_MODE_TYPE] = None
    # 'monitor-bandwidth',
    mtu: Optional[int] = None
    mtu_override: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("mtu-override", "mtu_override"),
        serialization_alias="mtu-override"
    )
    name: Optional[str] = None
    # 'ndiscforward',
    # 'netbios-forward',
    # 'netflow-sampler',
    # 'oid',
    # 'outbandwidth',
    # 'polling-interval',
    # 'pppoe-unnumbered-negotiate',
    # 'pptp-auth-type',
    # 'pptp-client',
    # 'pptp-password',
    # 'pptp-server-ip',
    # 'pptp-timeout',
    # 'preserve-session-route',
    # 'priority-override',
    # 'proxy-captive-portal',
    # 'reachable-time',
    # 'ring-rx',
    # 'ring-tx',
    role: Optional[INTERFACE_ROLE_TYPE] = None
    # 'sample-direction',
    # 'sample-rate',
    secondary_IP: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("secondary-IP", "secondary_IP"),
        serialization_alias="secondary-IP"
    )
    secondaryip: Optional[str] = None
    # 'security-exempt-list',
    # 'security-mac-auth-bypass',
    # 'security-mode',
    # 'sflow-sampler',
    # 'snmp-index',
    speed: Optional[INTERFACE_SPEED_TYPE] = None
    # 'spillover-threshold',
    src_check: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("src-check", "src_check"),
        serialization_alias="src-check"
    )
    status: Optional[INTERFACE_STATUS_TYPE] = None
    stpforward: Optional[ENABLE_DISABLE] = None
    stpforward_mode: Optional[INTERFACE_STPFORWARD_MODE_TYPE] = None
    # 'subst',
    # 'substitute-dst-mac',
    # 'swc-first-create',
    # 'swc-vlan',
    # 'switch-controller-arp-inspection',
    # 'switch-controller-feature',
    # 'switch-controller-igmp-snooping-fast-leave',
    # 'switch-controller-igmp-snooping-proxy',
    # 'switch-controller-mgmt-vlan',
    # 'switch-controller-netflow-collect',
    # 'switch-controller-rspan-mode',
    # 'switch-controller-source-ip',
    # 'system-id',
    # 'system-id-type',
    # 'tagging',
    tcp_mss: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("tcp-mss", "tcp_mss"),
        serialization_alias="tcp-mss"
    )
    # 'trust-ip6-1',
    # 'trust-ip6-2',
    # 'trust-ip6-3',
    type: Optional[INTERFACE_TYPE_TYPE] = None
    vdom: Optional[Union[Union[str, VDOM], List[Union[str, VDOM]]]] = None
    vindex: Optional[int] = None
    vlan_protocol: Optional[INTERFACE_VLAN_PROTO_TYPE] = None
    vlanid: Optional[int] = None
    # 'vlanforward',
    vrf: Optional[int] = Field(None, ge=0)
    vrrp: Optional[Union[str]] = None  # TODO: implement VRRP object
    vrrp_virtual_mac: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("vrrp-virtual-mac", "vrrp_virtual_mac"),
        serialization_alias="vrrp-virtual-mac"
    )
    # 'wccp',
    weight: Optional[int] = None
    # 'wifi-networks',
    # 'wins-ip'

    @property
    def get_url(self) -> str:
        # url = super().get_url
        if self.device is None:
            raise ValueError("Device parameter must be set!")
        url = self._url.replace("{device}", str(self.device))
        if self.fmg_interface is None:
            url = url.replace("/{fmg_interface}", "")
        else:
            url = url.replace("{fmg_interface}", self.interface)
        return url

    @field_validator("arpforward", "broadcast_forward", "icmp_accept_redirect", "icmp_send_redirect", "ipmac",
                     "lacp_ha_secondary", "mtu_override", "secondary_IP", "src_check", "stpforward", "vrrp_virtual_mac",
                     mode="before")
    def validate_allow_routing(cls, v) -> ENABLE_DISABLE:
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("vdom", mode="before")
    def validate_vdom(cls, vdom) -> Optional[List[str]]:
        if vdom is None:
            return vdom
        if isinstance(vdom, VDOM):
            return [vdom.name]
        if isinstance(vdom, list):
            if vdom and isinstance(vdom[0], str):
                return vdom
            if vdom and isinstance(vdom[0], VDOM):
                return [data.name for data in vdom]
            if not vdom:
                return vdom
        raise ValueError(f"Invalid vdom data {vdom}")

    @field_validator("ip", "management_ip", "secondaryip")
    def standardize_subnet(cls, v):
        """validator: x.x.x.x/y.y.y.y -> x.x.x.x/y

        API use this list form: ["1.2.3.4", "255.255.255.0"]
        Human use this form: "1.2.3.4/24"
        """
        if v is None:
            return None
        if isinstance(v, list):
            return IPv4Interface("/".join(v)).compressed
        else:
            return IPv4Interface(v).compressed

    @field_validator("interface", mode="before")
    def validate_interface(cls, v) -> List[str]:
        if isinstance(v, str):
            return [v]
        if isinstance(v, DeviceInterface):
            return [v.name]
        if isinstance(v, list):
            if v and isinstance(v[0], str):
                return v
            elif v and isinstance(v[0], DeviceInterface):
                return [device.name for device in v]
            return []
        raise ValueError(f"Invalid interface data {v}")


class DeviceZone(FMGObject):
    """Device zone

    """
    _url = "/pm/config/device/{device}/{scope}/system/zone/{zone}"
    _master_keys = ["name"]
    # URL fields
    device: Optional[Union[str, Device]] = Field(None, exclude=True)
    scope: Optional[Union[str, VDOM]] = Field("root", exclude=True)
    zone: Optional[Union[str, "DeviceZone"]] = Field(None, exclude=True)
    # API fields
    oid: Optional[int] = None
    tagging: Optional[Union[str, List[str]]] = None
    name: Optional[str] = None
    intrazone: Optional[PERMIT_DENY] = None
    interface: Optional[List[Union[str, DeviceInterface]]] = None
    description: Optional[str] = None

    @property
    def get_url(self) -> str:
        if not self.device:
            raise ValueError("Device parameter must be set!")
        scope = str(self.scope) if self.scope else None
        if scope != "global":
            scope = f"vdom/{scope}"
        url = self._url.replace("{device}", str(self.device))
        url = url.replace("{scope}", scope)
        if self.zone is None:
            url = url.replace("/{zone}", "")
        else:
            url = url.replace("{zone}", str(self.zone))
        return url

    @field_validator("interface", mode="before")
    def validate_interface(cls, v) -> List[str]:
        if isinstance(v, str):
            return [v]
        if isinstance(v, DeviceInterface):
            return [v.name]
        if isinstance(v, list):
            if v and isinstance(v[0], str):
                return v
            elif v and isinstance(v[0], DeviceInterface):
                return [device.name for device in v]
            return []
        raise ValueError(f"Invalid interface data {v}")