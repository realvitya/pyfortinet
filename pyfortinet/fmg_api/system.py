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
SMS_SERVER = Literal["fortiguard", "custom"]
TWO_FACTOR = Literal["disable", "fortitoken", "email", "sms", "fortitoken-cloud"]
TWO_FACTOR_AUTH = Literal["fortitoken", "email", "sms"]
TWO_FACTOR_NOTIFY = Literal["email", "sms"]


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
    # defaultgw: Optional[ENABLE_DISABLE] = None,
    description: Optional[str] = None
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
    member: Optional[List[str]] = None
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
    secondaryip: Optional[Union[str, List[str]]] = None
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


class SystemAdmin(FMGObject):
    """System administrator

    Attributes:
        accprofile:
        accprofile-override:
        allow-remove-admin-session:
        comments:
        email-to (str): This administrator's email address.
        force-password-change (str): Enable/disable force password change on next login.
        fortitoken (str): This administrator's FortiToken serial number.
        guest-auth (str): Enable/disable guest authentication.
        guest-lang (str): Guest management portal language.
        guest-usergroups: Select guest user groups.
        gui-default-dashboard-template: The default dashboard template.
        gui-ignore-invalid-signature-version (str): FortiOS image build version to ignore invalid signature warning for.
        gui-ignore-release-overview-version (str): FortiOS version to ignore release overview prompt for.
        history0 (list(str)):
        history1 (list(str)):
        ip6-trusthost1 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost2 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost3 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost4 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost5 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost6 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost7 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost8 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost9 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        ip6-trusthost10 (str): Any IPv6 address from which the administrator can connect to the FortiGate unit.
                              Default allows access from any IPv6 address.
        name (str): Username.
        password (str): Admin user password.
        password-expire (str): Password expire time.
        peer-auth: Set to enable peer certificate authentication (for HTTPS admin access).
        peer-group: Name of peer group defined under config user group which has PKI members. Used for peer certificate
                    authentication (for HTTPS admin access).
        radius-vdom-override:
        remote-auth (str): Enable/disable authentication using a remote RADIUS, LDAP, or TACACS+ server.
        remote-group: User group name used for remote auth.
        schedule: Firewall schedule used to restrict when the administrator can log in. No schedule means no
                  restrictions.
        sms-custom-server: Custom SMS server to send SMS messages to.
        sms-phone: Phone number on which the administrator receives SMS messages.
        sms-server: Send SMS messages using the FortiGuard SMS server or a custom server.
        ssh-certificate: Select the certificate to be used by the FortiGate for authentication with an SSH client.
        ssh-public-key1: Public key of an SSH client. The client is authenticated without being asked for credentials.
                         Create the public-private key pair in the SSH client application.
        ssh-public-key2: Public key of an SSH client. The client is authenticated without being asked for credentials.
                         Create the public-private key pair in the SSH client application.
        ssh-public-key3: Public key of an SSH client. The client is authenticated without being asked for credentials.
                         Create the public-private key pair in the SSH client application.
        trusthost1: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost2: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost3: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost4: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost5: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost6: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost7: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost8: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost9: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        trusthost10: Any IPv4 address or subnet address and netmask from which the administrator can connect to the
                    FortiGate unit. Default allows access from any IPv4 address.
        two-factor: Enable/disable two-factor authentication.
        two-factor-authentication: Authentication method by FortiToken Cloud.
        two-factor-notification: Notification method for user activation by FortiToken Cloud.
        vdom: Virtual domain(s) that the administrator can access.
        vdom-override: Enable to use the names of VDOMs provided by the remote authentication server to control the
                       VDOMs that this administrator can access.
        wildcard: Enable/disable wildcard RADIUS authentication.
    """
    _url = "/pm/config/device/{device}/global/system/admin/{admin}"
    _master_keys = ["name", "device"]
    # URL fields
    device: Optional[str] = Field(None, exclude=True)
    admin: Optional[str] = Field(None, exclude=True)
    # API fields
    accprofile: Optional[Union[str, List[str]]] = None
    accprofile_override: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("accprofile-override", "accprofile_override"),
        serialization_alias="accprofile-override",
    )

    allow_remove_admin_session: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("allow-remove-admin-session", "allow_remove_admin_session"),
        serialization_alias="allow-remove-admin-session",
    )
    comments: Optional[str] = None
    email_to: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("email-to", "email_to"),
        serialization_alias="email-to",
    )
    force_password_change: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("force-password-change", "force_password_change"),
        serialization_alias="force-password-change",
    )
    fortitoken: Optional[Union[str, List[str]]] = None  # TODO: implement FORTITOKEN model
    guest_auth:Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("guest-auth", "guest_auth"),
        serialization_alias="guest-auth",
    )
    guest_lang: Optional[Union[str, List[str]]] = Field(  # TODO: implement GUESTLANG model
        None,
        validation_alias=AliasChoices("guest-lang", "guest_lang"),
        serialization_alias="guest-lang",
    )
    guest_usergroups: Optional[Union[str, List[str]]] = Field(  # TODO: implement GUEST_USERGROUPS
        None,
        validation_alias=AliasChoices("guest-usergroups", "guest_usergroups"),
        serialization_alias="guest-usergroups",
    )
    gui_default_dashboard_template: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("gui-default-dashboard-template", "gui_default_dashboard_template"),
        serialization_alias="gui-default-dashboard-template",
    )
    gui_ignore_invalid_signature_version: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("gui-ignore-invalid-signature-version", "gui_ignore_invalid_signature_version"),
        serialization_alias="gui-ignore-invalid-signature-version",
    )
    gui_ignore_release_overview_version: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("gui-ignore-release-overview-version", "gui_ignore_release_overview_version"),
        serialization_alias="gui-ignore-release-overview-version",
    )
    history0: Optional[Union[str, List[str]]] = None
    history1: Optional[Union[str, List[str]]] = None
    ip6_trusthost1: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost1", "ip6_trusthost1"),
        serialization_alias="ip6-trusthost1",
    )
    ip6_trusthost2: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost2", "ip6_trusthost2"),
        serialization_alias="ip6-trusthost2",
    )
    ip6_trusthost3: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost3", "ip6_trusthost3"),
        serialization_alias="ip6-trusthost3",
    )
    ip6_trusthost4: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost4", "ip6_trusthost4"),
        serialization_alias="ip6-trusthost4",
    )
    ip6_trusthost5: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost5", "ip6_trusthost5"),
        serialization_alias="ip6-trusthost5",
    )
    ip6_trusthost6: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost6", "ip6_trusthost6"),
        serialization_alias="ip6-trusthost6",
    )
    ip6_trusthost7: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost7", "ip6_trusthost7"),
        serialization_alias="ip6-trusthost7",
    )
    ip6_trusthost8: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost8", "ip6_trusthost8"),
        serialization_alias="ip6-trusthost8",
    )
    ip6_trusthost9: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost9", "ip6_trusthost9"),
        serialization_alias="ip6-trusthost9",
    )
    ip6_trusthost10: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip6-trusthost10", "ip6_trusthost10"),
        serialization_alias="ip6-trusthost10",
    )
    name: Optional[str] = None
    password: Optional[Union[str, List[str]]] = None
    password_expire: Optional[Union[str, List[str]]] = Field(
        None,
        validation_alias=AliasChoices("password-expire", "password_expire"),
        serialization_alias="password-expire",
    )
    peer_auth: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("peer-auth", "peer_auth"),
        serialization_alias="peer-auth",
    )
    peer_group: Optional[Union[str, List[str]]] = Field(
        None,
        validation_alias=AliasChoices("peer-group", "peer_group"),
        serialization_alias="peer-group",
    )
    radius_vdom_override: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("radius-vdom-override", "radius_vdom_override"),
        serialization_alias="radius-vdom-override",
    )
    remote_auth: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("remote-auth", "remote_auth"),
        serialization_alias="remote-auth",
    )
    remote_group: Optional[Union[str, List[str]]] = Field(  # TODO: implement REMOTE_USERGROUP
        None,
        validation_alias=AliasChoices("remote-group", "remote_group"),
        serialization_alias="remote-group",
    )
    schedule: Optional[str] = None  # might need some research if we could do validation
    sms_custom_server: Optional[Union[str, List[str]]] = Field(
        None,
        validation_alias=AliasChoices("sms-custom-server", "sms_custom_server"),
        serialization_alias="sms-custom-server",
    )
    sms_phone: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("sms-phone", "sms_phone"),
        serialization_alias="sms-phone",
    )
    sms_server: Optional[SMS_SERVER] = Field(
        None,
        validation_alias=AliasChoices("sms-server", "sms_server"),
        serialization_alias="sms-server",
    )
    ssh_certificate: Optional[Union[str, List[str]]] = Field(  # TODO: implement SSH_CERTIFICATE model
        None,
        validation_alias=AliasChoices("ssh-certificate", "ssh_certificate"),
        serialization_alias="ssh-certificate",
    )
    ssh_public_key1: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ssh-public-key1", "ssh_public_key1"),
        serialization_alias="ssh-public-key1",
    )
    ssh_public_key2: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ssh-public-key2", "ssh_public_key2"),
        serialization_alias="ssh-public-key2",
    )
    ssh_public_key3: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ssh-public-key3", "ssh_public_key3"),
        serialization_alias="ssh-public-key3",
    )
    trusthost1: Optional[Union[str, List[str]]] = None
    trusthost2: Optional[Union[str, List[str]]] = None
    trusthost3: Optional[Union[str, List[str]]] = None
    trusthost4: Optional[Union[str, List[str]]] = None
    trusthost5: Optional[Union[str, List[str]]] = None
    trusthost6: Optional[Union[str, List[str]]] = None
    trusthost7: Optional[Union[str, List[str]]] = None
    trusthost8: Optional[Union[str, List[str]]] = None
    trusthost9: Optional[Union[str, List[str]]] = None
    trusthost10: Optional[Union[str, List[str]]] = None
    two_factor: Optional[TWO_FACTOR] = Field(
        None,
        validation_alias=AliasChoices("two-factor", "two_factor"),
        serialization_alias="two-factor",
    )
    two_factor_authentication: Optional[TWO_FACTOR_AUTH] = Field(
        None,
        validation_alias=AliasChoices("two-factor-authentication", "two_factor_authentication"),
        serialization_alias="two-factor-authentication",
    )
    two_factor_notification: Optional[TWO_FACTOR_NOTIFY] = Field(
        None,
        validation_alias=AliasChoices("two-factor-notification", "two_factor_notification"),
        serialization_alias="two-factor-notification",
    )
    vdom: Optional[Union[str, VDOM, List[Union[str,VDOM]]]] = None
    vdom_override: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("vdom-override", "vdom_override"),
        serialization_alias="vdom-override",
    )
    wildcard: Optional[ENABLE_DISABLE] = None

    @property
    def get_url(self):
        if not self.device:
            raise ValueError("Please specify `device` field or assign object to FMG!")
        url = self._url.replace("{device}", self.device)
        if not self.admin:  # specifying existing user is optional and required to rename and delete only
            return url.replace("/{admin}", "")
        return url.replace("{admin}", self.admin)
