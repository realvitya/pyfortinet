"""Fortinet Policy object"""

from typing import Literal, Union, Optional, List, Any

from pydantic import BaseModel, AliasChoices, Field, field_validator, field_serializer

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.firewall import Address, AddressGroup, ServiceCustom, ServiceGroup

POLICY_ACTION = Literal["deny", "accept", "ipsec", "ssl-vpn", "redirect", "isolate"]
ENABLE_DISABLE = Literal["disable", "enable"]
OR_AND = Literal["or", "and"]
INSPECTION_MODE = Literal["proxy", "flow"]
NGFW_MODE = Literal["profile-based", "policy-based"]
POLICY_OFFLOAD_LEVEL = Literal["disable", "default", "dos-offload", "full-offload"]
POLICY_DISCLAIMER = Literal["disable", "enable", "user", "domain", "policy"]
FIREWALL_SESSION_DIRTY_TYPE = Literal["check-all", "check-new"]
GEOIP_MATCH_TYPE = Literal["physical-location", "registered-location"]
INSPECTION_MODE_TYPE = Literal["proxy", "flow"]
LOG_TRAFFIC_TYPE = Literal["disable", "enable", "all", "utm"]
PROFILE_TYPE = Literal["single", "group"]
REPUTATION_DIRECTION_TYPE = Literal["source", "destination"]
TCP_SESSION_WO_SYN_TYPE = Literal["all", "data-only", "disable"]


# noinspection SpellCheckingInspection
class PackageSettings(BaseModel):
    """Package Settings class

    Attributes:

    """

    central_nat: Optional[ENABLE_DISABLE] = Field(
        None, validation_alias=AliasChoices("central-nat", "central_nat"), serialization_alias="central-nat"
    )
    consolidated_firewall_mode: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("consolidated-firewall-mode", "consolidated_firewall_mode"),
        serialization_alias="consolidated-firewall-mode",
    )
    firewall_mode: Optional[ENABLE_DISABLE] = Field(
        None, validation_alias=AliasChoices("firewall-mode", "firewall_mode"), serialization_alias="firewall-mode"
    )
    fwpolicy_implicit_log: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fwpolicy-implicit-log", "fwpolicy_implicit_log"),
        serialization_alias="fwpolicy-implicit-log",
    )
    fwpolicy6_implicit_log: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fwpolicy6-implicit-log", "fwpolicy6_implicit_log"),
        serialization_alias="fwpolicy6-implicit-log",
    )
    inspection_mode: Optional[INSPECTION_MODE] = Field(
        None, validation_alias=AliasChoices("inspection-mode", "inspection_mode"), serialization_alias="inspection_mode"
    )
    ngfw_mode: Optional[NGFW_MODE] = Field(
        None, validation_alias=AliasChoices("ngfw-mode", "ngfw_mode"), serialization_alias="ngfw-mode"
    )
    policy_offload_level: Optional[POLICY_OFFLOAD_LEVEL] = Field(
        None,
        validation_alias=AliasChoices("policy-offload-level", "policy_offload_level"),
        serialization_alias="policy-offload-level",
    )
    ssl_ssh_profile: Optional[str] = None  # TODO: implement SSLSSHProfile

    @field_validator(
        "central_nat",
        "consolidated_firewall_mode",
        "firewall_mode",
        "fwpolicy_implicit_log",
        "fwpolicy6_implicit_log",
        mode="before",
    )
    def standardize_enabled_disabled(cls, v):
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("inspection_mode", mode="before")
    def standardize_inspection_mode(cls, v):
        return INSPECTION_MODE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("ngfw_mode", mode="before")
    def standardize_ngfw_mode(cls, v):
        return NGFW_MODE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("policy_offload_level", mode="before")
    def standardize_policy_offload_level(cls, v):
        return POLICY_OFFLOAD_LEVEL.__dict__.get("__args__")[v] if isinstance(v, int) else v


POLICYPACKAGETYPE = Literal["pkg", "folder"]


class PolicyPackage(FMGObject):
    """Policy Package class

    Attributes:
        name:
        obj_ver:
        oid:
        package_settings:
        scope_member:
        subobj:
        type:
    """

    _url = "/pm/pkg/{scope}"
    _master_keys = ["name"]
    name: Optional[str] = None
    obj_ver: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("obj ver", "obj_ver"),
        serialization_alias="obj ver"
    )
    oid: Optional[int] = None
    package_settings: Optional[PackageSettings] = Field(
        None,
        validation_alias=AliasChoices("package settings", "package_settings"),
        serialization_alias="package settings"
    )
    scope_member: Optional[List[Scope]] = None
    subobj: Optional[List[Any]] = None  # TODO: this is for folder type. Needs testing!
    type: Optional[POLICYPACKAGETYPE] = "pkg"


# noinspection SpellCheckingInspection
class Policy(FMGObject):
    """Policy class

    Configure IPv4/IPv6 policies.
    When configuring policy within policy package, use (/pm/config/adom/pkg/).
    When configuring policy for a policy block, use (/pm/config/adom/pblock/).

    Attributes:
        adom (str): adom to use (default is specfied by fmg object)
        pkg (str): PolicyPackage selection
        policy_block (int):
            Assigned policy block. When this attribute is set, the policy represent a policy block,
            and all other attributes are ignored.
            This attribute is not available when configuring policy inside a policy block.

        action (POLICY_ACTION):
            Policy action.

        anti_replay (ENABLE_DISABLE):
            Enable/disable anti-replay check.

        application_list:
            Name of an existing Application list.

        auth_cert:
            HTTPS server certificate for policy authentication.

        auth_path (str):
            Enable/disable authentication-based routing.

        auth_redirect_addr (str):
            HTTP-to-HTTPS redirect address for firewall authentication.
        av_profile (str): Name of an existing Antivirus profile.
        block_notification (str): Enable/disable block notification.
        captive_portal_exempt (str): Enable to exempt some users from the captive portal.
        casb_profile (str): Name of an existing CASB profile.
        comments (str): Comment.
        custom_log_fields (List[str]): Custom fields to append to log messages for this policy.
        decrypted_traffic_mirror (str): Decrypted traffic mirror.
        delay_tcp_npu_session (str): Enable TCP NPU session delay to guarantee packet order of 3-way handshake.
        diameter_filter_profile (str): Name of an existing Diameter filter profile.
        diffserv_copy (str):
            Enable to copy packet's DiffServ values from session's original direction to its reply direction.
        diffserv_forward (str): Enable to change packet's DiffServ values to the specified diffservcode-forward value.
        diffserv_reverse (str):
            Enable to change packet's reverse (reply) DiffServ values to the specified diffservcode-rev value.
        diffservcode_forward (str): Change packet's DiffServ to this value.
        diffservcode_rev (str): Change packet's reverse (reply) DiffServ to this value.
        disclaimer (str): Enable/disable user authentication disclaimer.
        dlp_profile (str): Name of an existing DLP profile.
        dnsfilter_profile (str): Name of an existing DNS filter profile.
        dsri (str): Enable DSRI to ignore HTTP server responses.
        dstaddr (List[str]): Destination IPv4 address and address group names.
        dstaddr_negate (str): When enabled dstaddr specifies what the destination address must NOT be.
        dstaddr6 (List[str]): Destination IPv6 address name and address group names.
        dstaddr6_negate (str): When enabled dstaddr6 specifies what the destination address must NOT be.
        dstintf (List[str]): Outgoing (egress) interface.
        dynamic_shaping (str): Enable/disable dynamic RADIUS defined traffic shaping.
        email_collect (str): Enable/disable email collection.
        emailfilter_profile (str): Name of an existing email filter profile.
        fec (str): Enable/disable Forward Error Correction on traffic matching this policy on a FEC device.
        file_filter_profile (str): Name of an existing file-filter profile.
        firewall_session_dirty (str): How to handle sessions if the configuration of this firewall policy changes.
        fixedport (str): Enable to prevent source NAT from changing a session's source port.
        fsso_agent_for_ntlm (str): FSSO agent to use for NTLM authentication.
        fsso_groups (List[str]): Names of FSSO groups.
        geoip_anycast (str): Enable/disable recognition of anycast IP addresses using the geography IP database.
        geoip_match (str): Match geography address based either on its physical location or registered location.
        global_label (str): Label for the policy that appears when the GUI is in Global View mode.
        groups (List[str]): Names of user groups that can authenticate with this policy.
        http_policy_redirect (str): Redirect HTTP(S) traffic to matching transparent web proxy policy.
        icap_profile (str): Name of an existing ICAP profile.
        identity_based_route (str): Name of identity-based routing rule.
        inbound (str): Policy-based IPsec VPN: only traffic from the remote network can initiate a VPN.
        inspection_mode (str): Policy inspection mode (Flow/proxy). Default is Flow mode.
        internet_service (str):
            Enable/disable use of Internet Services for this policy.
            If enabled, destination address and service are not used.
        internet_service_custom (List[str]): Custom Internet Service name.
        internet_service_custom_group (List[str]): Custom Internet Service group name.
        internet_service_group (List[str]): Internet Service group name.
        internet_service_name (List[str]): Internet Service name.
        internet_service_negate (str): When enabled internet-service specifies what the service must NOT be.
        internet_service_src (str):
            Enable/disable use of Internet Services in source for this policy. If enabled, source address is not used.
        internet_service_src_custom (List[str]): Custom Internet Service source name.
        internet_service_src_custom_group (List[str]): Custom Internet Service source group name.
        internet_service_src_group (List[str]): Internet Service source group name.
        internet_service_src_name (List[str]): Internet Service source name.
        internet_service_src_negate (str): When enabled internet-service-src specifies what the service must NOT be.
        internet_service6 (str):
            Enable/disable use of IPv6 Internet Services for this policy.
            If enabled, destination address and service are not used.
        internet_service6_custom (List[str]): Custom IPv6 Internet Service name.
        internet_service6_custom_group (List[str]): Custom Internet Service6 group name.
        internet_service6_group (List[str]): Internet Service group name.
        internet_service6_name (List[str]): IPv6 Internet Service name.
        internet_service6_negate (str): When enabled internet-service6 specifies what the service must NOT be.
        internet_service6_src (str):
            Enable/disable use of IPv6 Internet Services in source for this policy.
            If enabled, source address is not used.
        internet_service6_src_custom (List[str]): Custom IPv6 Internet Service source name.
        internet_service6_src_custom_group (List[str]): Custom Internet Service6 source group name.
        internet_service6_src_group (List[str]): Internet Service6 source group name.
        internet_service6_src_name (List[str]): IPv6 Internet Service source name.
        internet_service6_src_negate (str): When enabled internet-service6-src specifies what the service must NOT be.
        ip_version_type (str): IP version of the policy.
        ippool (str): Enable to use IP Pools for source NAT.
        ips_sensor (str): Name of an existing IPS sensor.
        ips_voip_filter (str): Name of an existing VoIP (ips) profile.
        label (str): Label for the policy that appears when the GUI is in Section View mode.
        logtraffic (str): Enable or disable logging. Log all sessions or security profile sessions.
        logtraffic_start (str): Record logs when a session starts.
        match_vip (str): Enable to match packets that have had their destination addresses changed by a VIP.
        match_vip_only (str):
            Enable/disable matching of only those packets that have had their destination addresses changed by a VIP.
        name (str): Policy name.
        nat (str): Enable/disable source NAT.
        nat46 (str): Enable/disable NAT46.
        nat64 (str): Enable/disable NAT64.
        natinbound (str): Policy-based IPsec VPN: apply destination NAT to inbound traffic.
        natip (str): Policy-based IPsec VPN: source NAT IP address for outgoing traffic.
        natoutbound (str): Policy-based IPsec VPN: apply source NAT to outbound traffic.
        network_service_dynamic (List[str]): Dynamic Network Service name.
        network_service_src_dynamic (List[str]): Dynamic Network Service source name.
        ntlm (str): Enable/disable NTLM authentication.
        ntlm_enabled_browsers (List[str]): HTTP-User-Agent value of supported browsers.
        ntlm_guest (str): Enable/disable NTLM guest user access.
        outbound (str): Policy-based IPsec VPN: only traffic from the internal network can initiate a VPN.
        passive_wan_health_measurement (str):
            Enable/disable passive WAN health measurement. When enabled, auto-asic-offload is disabled.
        pcp_inbound (str): Enable/disable PCP inbound DNAT.
        pcp_outbound (str): Enable/disable PCP outbound SNAT.
        pcp_poolname (List[str]): PCP pool names.
        per_ip_shaper (str): Per-IP traffic shaper.
        permit_any_host (str): Accept UDP packets from any host.
        permit_stun_host (str): Accept UDP packets from any Session Traversal Utilities for NAT (STUN) host.
        policy_behaviour_type (str): Behaviour of the policy.
        policy_expiry (str): Enable/disable policy expiry.
        policy_expiry_date (str): Policy expiry date (YYYY-MM-DD HH:MM:SS).
        policy_expiry_date_utc (str): Policy expiry date and time, in epoch format.
        policyid (int): Policy ID (0 - 4294967294).
        poolname (List[str]): IP Pool names.
        poolname6 (List[str]): IPv6 pool names.
        profile_group (str): Name of profile group.
        profile_protocol_options (str): Name of an existing Protocol options profile.
        profile_type (str):
            Determine whether the firewall policy allows security profile groups or single profiles only.
        radius_mac_auth_bypass (str):
            Enable MAC authentication bypass. The bypassed MAC address must be received from RADIUS server.
        redirect_url (str): URL users are directed to after seeing and accepting the disclaimer or authenticating.
        replacemsg_override_group (str): Override the default replacement message group for this policy.
        reputation_direction (str): Direction of the initial traffic for reputation to take effect.
        reputation_direction6 (str): Direction of the initial traffic for IPv6 reputation to take effect.
        reputation_minimum (int): Minimum Reputation to take action.
        reputation_minimum6 (int): IPv6 Minimum Reputation to take action.
        rtp_addr (List[str]): Address names if this is an RTP NAT policy.
        rtp_nat (str): Enable Real Time Protocol (RTP) NAT.
        schedule (str): Schedule name.
        schedule_timeout (str):
            Enable to force current sessions to end when the schedule object times out.
            Disable allows them to end from inactivity.
        sctp_filter_profile (str): Name of an existing SCTP filter profile.
        send_deny_packet (str): Enable to send a reply to a blocked connection attempt.
        service (List[str]): Service names and service group names.
        service_negate (str): When enabled service specifies what the service must NOT be.
        session_ttl (str):
            TTL in seconds for sessions accepted by this policy (0 means use the system default session TTL).
        sgt (List[int]): Security group tags.
        sgt_check (ENABLE_DISABLE): Enable/disable security group tags (SGT) check.
        src_vendor_mac (List[str]): Vendor MAC source ID.


    """
    _url = "/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy"
    _master_keys = ["policyid"]
    # URL fields
    adom: Optional[str] = Field(None, exclude=True)
    pkg: Optional[str] = Field(None, exclude=True)
    # API fields
    policy_block: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("_policy_block", "policy_block"),
        serialization_alias="_policy_block",
    )
    action: Optional[POLICY_ACTION] = None
    anti_replay: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("anti-replay", "anti_replay"),
        serialization_alias="anti-replay",
    )
    application_list: Optional[Union[str, list]] = Field(  # TODO: add ApplicationList later when implemented
        None,
        validation_alias=AliasChoices("application-list", "application_list"),
        serialization_alias="application-list",
    )
    auth_cert: Optional[str] = Field(  # TODO: add AuthCert later when implemented
        None,
        validation_alias=AliasChoices("auth-cert", "auth_cert"),
        serialization_alias="auth-cert",
    )
    auth_path: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("auth-path", "auth_path"),
        serialization_alias="auth-path",
    )
    auth_redirect_addr: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("auth-redirect-addr", "auth_redirect_addr"),
        serialization_alias="auth-redirect-addr",
    )
    av_profile: Optional[Union[str, list]] = Field(  # TODO: add AVProfile later when implemented
        None,
        validation_alias=AliasChoices("av-profile", "av_profile"),
        serialization_alias="av-profile",
    )
    block_notification: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("block-notification", "block_notification"),
        serialization_alias="block-notification",
    )
    captive_portal_exempt: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("captive-portal-exempt", "captive_portal_exempt"),
        serialization_alias="captive-portal-exempt",
    )
    capture_packet: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("capture-packet", "capture_packet"),
        serialization_alias="capture-packet",
    )
    casb_profile: Optional[str] = Field(  # TODO: add CASBProfile later when implemented
        None,
        validation_alias=AliasChoices("casb-profile", "casb_profile"),
        serialization_alias="casb-profile",
    )
    comments: Optional[str] = None
    custom_log_fields: Optional[List[str]] = Field(  # TODO: add LogCustomFields later when implemented
        None,
        validation_alias=AliasChoices("custom-log-fields", "custom_log_fields"),
        serialization_alias="custom-log-fields",
    )
    decrypted_traffic_mirror: Optional[str] = Field(  # TODO: add TrafficMirror later when implemented
        None,
        validation_alias=AliasChoices("decrypted-traffic-mirror", "decrypted_traffic_mirror"),
        serialization_alias="decrypted-traffic-mirror",
    )
    delay_tcp_npu_session: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("delay-tcp-npu-session", "delay_tcp_npu_session"),
        serialization_alias="delay-tcp-npu-session",
    )

    diameter_filter_profile: Optional[str] = Field(  # TODO: add DiameterFilterProfile later when implemented
        None,
        validation_alias=AliasChoices("diameter-filter-profile", "diameter_filter_profile"),
        serialization_alias="diameter-filter-profile",
    )
    diffserv_copy: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("diffserv-copy", "diffserv_copy"),
        serialization_alias="diffserv-copy",
    )
    diffserv_forward: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("diffserv-forward", "diffserv_forward"),
        serialization_alias="diffserv-forward",
    )
    diffserv_reverse: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("diffserv-reverse", "diffserv_reverse"),
        serialization_alias="diffserv-reverse",
    )
    diffservcode_forward: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("diffservcode-forward", "diffservcode_forward"),
        serialization_alias="diffservcode-forward",
    )
    diffservcode_rev: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("diffservcode-rev", "diffservcode_rev"),
        serialization_alias="diffservcode-rev",
    )
    disclaimer: Optional[POLICY_DISCLAIMER] = None
    dlp_profile: Optional[Union[str, list]] = Field(  # TODO: add DLPProfile later when implemented
        None,
        validation_alias=AliasChoices("dlp-profile", "dlp_profile"),
        serialization_alias="dlp-profile",
    )
    dnsfilter_profile: Optional[Union[str, list]] = Field(  # TODO: add DNSProfile later when implemented
        None,
        validation_alias=AliasChoices("dnsfilter-profile", "dnsfilter_profile"),
        serialization_alias="dnsfilter-profile",
    )
    dsri: Optional[ENABLE_DISABLE] = None
    dstaddr: Optional[List[Union[str, Address, AddressGroup]]] = None
    dstaddr_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("dstaddr-negate", "dstaddr_negate"),
        serialization_alias="dstaddr-negate",
    )
    dstaddr6: Optional[List[str]] = None  # TODO: add Address6 or AddressGroup6 later when implemented
    dstaddr6_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("dstaddr6-negate", "dstaddr6_negate"),
        serialization_alias="dstaddr6-negate",
    )
    dstintf: Optional[List[str]] = None  # TODO: add Interface later when implemented
    dynamic_shaping: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("dynamic-shaping", "dynamic_shaping"),
        serialization_alias="dynamic-shaping",
    )
    email_collect: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("email-collect", "email_collect"),
        serialization_alias="email-collect",
    )
    emailfilter_profile: Optional[Union[str, list]] = Field(  # TODO: add EmailFilterProfile later when implemented
        None,
        validation_alias=AliasChoices("emailfilter-profile", "emailfilter_profile"),
        serialization_alias="emailfilter-profile",
    )
    fec: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fec", "fec"),
        serialization_alias="fec",
    )
    file_filter_profile: Optional[List[str]] = Field(  # TODO: add FileFilterProfile later when implemented
        None,
        validation_alias=AliasChoices("file-filter-profile", "file_filter_profile"),
        serialization_alias="file-filter-profile",
    )
    firewall_session_dirty: Optional[FIREWALL_SESSION_DIRTY_TYPE] = Field(
        None,
        validation_alias=AliasChoices("firewall-session-dirty", "firewall_session_dirty"),
        serialization_alias="firewall-session-dirty",
    )
    fixedport: Optional[ENABLE_DISABLE] = None
    fsso_agent_for_ntlm: Optional[List[str]] = Field(  # TODO: add SSOAgent later when implemented
        None,
        validation_alias=AliasChoices("fsso-agent-for-ntlm", "fsso_agent_for_ntlm"),
        serialization_alias="fsso-agent-for-ntlm",
    )
    fsso_groups: Optional[List[str]] = Field(  # TODO: add FSSOGroup later when implemented
        None,
        validation_alias=AliasChoices("fsso-groups", "fsso_groups"),
        serialization_alias="fsso-groups",
    )
    geoip_anycast: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("geoip-anycast", "geoip_anycast"),
        serialization_alias="geoip-anycast",
    )
    geoip_match: Optional[GEOIP_MATCH_TYPE] = Field(
        None,
        validation_alias=AliasChoices("geoip-match", "geoip_match"),
        serialization_alias="geoip-match",
    )
    global_label: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("global-label", "global_label"),
        serialization_alias="global-label",
    )
    groups: Optional[List[str]] = None  # TODO: add UserGroup later when implemented
    http_policy_redirect: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("http-policy-redirect", "http_policy_redirect"),
        serialization_alias="http-policy-redirect",
    )
    icap_profile: Optional[str] = Field(  # TODO: add ICAPProfile later when implemented
        None,
        validation_alias=AliasChoices("icap-profile", "icap_profile"),
        serialization_alias="icap-profile",
    )
    identity_based_route: Optional[str] = Field(  # TODO: add IdentityRoute later when implemented
        None,
        validation_alias=AliasChoices("identity-based-route", "identity_based_route"),
        serialization_alias="identity-based-route",
    )
    inbound: Optional[ENABLE_DISABLE] = None
    inspection_mode: Optional[INSPECTION_MODE_TYPE] = Field(
        None,
        validation_alias=AliasChoices("inspection-mode", "inspection_mode"),
        serialization_alias="inspection-mode",
    )
    internet_service: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("internet-service", "internet_service"),
        serialization_alias="internet-service",
    )
    internet_service_custom: Optional[List[str]] = Field(
        # TODO: add InternetServiceCustom later when implemented
        None,
        validation_alias=AliasChoices("internet-service-custom", "internet_service_custom"),
        serialization_alias="internet-service-custom",
    )
    internet_service_custom_group: Optional[List[str]] = Field(
        # TODO: add InternetServiceCustomGroup later when implemented
        None,
        validation_alias=AliasChoices("internet-service-custom-group", "internet_service_custom_group"),
        serialization_alias="internet-service-custom-group",
    )
    internet_service_group: Optional[List[str]] = Field(
        # TODO: add InternetServiceGroup later when implemented
        None,
        validation_alias=AliasChoices("internet-service-group", "internet_service_group"),
        serialization_alias="internet-service-group",
    )
    internet_service_name: Optional[List[str]] = Field(
        # TODO: add InternetServiceName later when implemented
        None,
        validation_alias=AliasChoices("internet-service-name", "internet_service_name"),
        serialization_alias="internet-service-name",
    )
    internet_service_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("internet-service-negate", "internet_service_negate"),
        serialization_alias="internet-service-negate",
    )
    internet_service_src: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("internet-service-src", "internet_service_src"),
        serialization_alias="internet-service-src",
    )
    internet_service_src_custom: Optional[List[str]] = Field(
        # TODO: add InternetServiceCustom later when implemented
        None,
        validation_alias=AliasChoices("internet-service-src-custom", "internet_service_src_custom"),
        serialization_alias="internet-service-src-custom",
    )
    internet_service_src_custom_group: Optional[List[str]] = Field(
        # TODO: add InternetServiceCustomGroup when implemented
        None,
        validation_alias=AliasChoices("internet-service-src-custom-group", "internet_service_src_custom_group"),
        serialization_alias="internet-service-src-custom-group",
    )
    internet_service_src_group: Optional[List[str]] = Field(
        # TODO: add InternetServiceGroup when implemented
        None,
        validation_alias=AliasChoices("internet-service-src-group", "internet_service_src_group"),
        serialization_alias="internet-service-src-group",
    )
    internet_service_src_name: Optional[List[str]] = Field(
        # TODO: add InternetServiceName later when implemented
        None,
        validation_alias=AliasChoices("internet-service-src-name", "internet_service_src_name"),
        serialization_alias="internet-service-src-name",
    )
    internet_service_src_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("internet-service-src-negate", "internet_service_src_negate"),
        serialization_alias="internet-service-src-negate",
    )
    internet_service6: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("internet-service6", "internet_service6"),
        serialization_alias="internet-service6",
    )
    internet_service6_custom: Optional[List[str]] = Field(
        # TODO: Define the InternetService6Custom class and replace List[str]
        None,
        validation_alias=AliasChoices("internet-service6-custom", "internet_service6_custom"),
        serialization_alias="internet-service6-custom",
    )
    internet_service6_custom_group: Optional[List[str]] = Field(
        # TODO: Define the InternetService6CustomGroup class and replace List[str]
        None,
        validation_alias=AliasChoices("internet-service6-custom-group", "internet_service6_custom_group"),
        serialization_alias="internet-service6-custom-group",
    )
    internet_service6_group: Optional[List[str]] = Field(
        # TODO: Define the InternetService6Group class and replace List[str]
        None,
        validation_alias=AliasChoices("internet-service6-group", "internet_service6_group"),
        serialization_alias="internet-service6-group",
    )
    internet_service6_name: Optional[List[str]] = Field(
        # TODO: Define the InternetService6Name class and replace List[str]
        None,
        validation_alias=AliasChoices("internet-service6-name", "internet_service6_name"),
        serialization_alias="internet-service6-name",
    )
    internet_service6_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("internet-service6-negate", "internet_service6_negate"),
        serialization_alias="internet-service6-negate",
    )
    internet_service6_src: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("internet-service6-src", "internet_service6_src"),
        serialization_alias="internet-service6-src",
    )
    internet_service6_src_custom: Optional[List[str]] = Field(
        # TODO: Define the InternetService6SrcCustom class and replace List[str]
        None,
        validation_alias=AliasChoices("internet-service6-src-custom", "internet_service6_src_custom"),
        serialization_alias="internet-service6-src-custom",
    )
    internet_service6_src_custom_group: Optional[List[str]] = Field(
        # TODO: Define the InternetService6SrcCustomGroup class and replace List[str]
        None,
        validation_alias=AliasChoices("internet-service6-src-custom-group", "internet_service6_src_custom_group"),
        serialization_alias="internet-service6-src-custom-group",
    )
    internet_service6_src_group: Optional[List[str]] = Field(
        # TODO: Define the InternetService6SrcGroup class and replace List[str]
        None,
        validation_alias=AliasChoices("internet-service6-src-group", "internet_service6_src_group"),
        serialization_alias="internet-service6-src-group",
    )
    internet_service6_src_name: Optional[List[str]] = Field(
        # TODO: Define the InternetService6SrcName class and replace List[str]
        None,
        validation_alias=AliasChoices("internet-service6-src-name", "internet_service6_src_name"),
        serialization_alias="internet-service6-src-name",
    )
    internet_service6_src_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("internet-service6-src-negate", "internet_service6_src_negate"),
        serialization_alias="internet-service6-src-negate",
    )
    ip_version_type: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ip-version-type", "ip_version_type"),
        serialization_alias="ip-version-type",
    )
    ippool: Optional[ENABLE_DISABLE] = None
    ips_sensor: Optional[Union[str, list]] = Field(  # TODO: Define the IPSSensor class and use it here instead of str
        None,
        validation_alias=AliasChoices("ips-sensor", "ips_sensor"),
        serialization_alias="ips-sensor",
    )
    ips_voip_filter: Optional[List[str]] = Field(  # TODO: Define the VoIPProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("ips-voip-filter", "ips_voip_filter"),
        serialization_alias="ips-voip-filter",
    )
    label: Optional[str] = None
    logtraffic: Optional[LOG_TRAFFIC_TYPE] = None
    logtraffic_start: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("logtraffic-start", "logtraffic_start"),
        serialization_alias="logtraffic-start",
    )
    match_vip: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("match-vip", "match_vip"),
        serialization_alias="match-vip",
    )
    match_vip_only: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("match-vip-only", "match_vip_only"),
        serialization_alias="match-vip-only",
    )
    name: Optional[str] = None
    nat: Optional[ENABLE_DISABLE] = None
    nat46: Optional[ENABLE_DISABLE] = None
    nat64: Optional[ENABLE_DISABLE] = None
    natinbound: Optional[ENABLE_DISABLE] = None
    natip: Optional[List[Union[str, Address]]] = None
    natoutbound: Optional[ENABLE_DISABLE] = None
    # TODO: Define NetworkServiceDynamic class and use it here instead of List[str]
    network_service_dynamic: Optional[List[str]] = None
    # TODO: Define NetworkServiceSrcDynamic class and use it here instead of List[str]
    network_service_src_dynamic: Optional[List[str]] = None
    ntlm: Optional[ENABLE_DISABLE] = None
    ntlm_enabled_browsers: Optional[List[str]] = Field(
        None,
        validation_alias=AliasChoices("ntlm-enabled-browsers", "ntlm_enabled_browsers"),
        serialization_alias="ntlm-enabled-browsers",
    )
    ntlm_guest: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("ntlm-guest", "ntlm_guest"),
        serialization_alias="ntlm-guest",
    )
    outbound: Optional[ENABLE_DISABLE] = None
    passive_wan_health_measurement: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("passive-wan-health-measurement", "passive_wan_health_measurement"),
        serialization_alias="passive-wan-health-measurement",
    )
    pcp_inbound: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("pcp-inbound", "pcp_inbound"),
        serialization_alias="pcp-inbound",
    )
    pcp_outbound: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("pcp-outbound", "pcp_outbound"),
        serialization_alias="pcp-outbound",
    )
    pcp_poolname: Optional[List[str]] = Field(
        # TODO: Define the PCPPoolName class and use it here instead of List[str]
        None,
        validation_alias=AliasChoices("pcp-poolname", "pcp_poolname"),
        serialization_alias="pcp-poolname",
    )

    per_ip_shaper: Optional[List[str]] = Field(
        # TODO: Define the PerIPShaper class and use it here instead of str
        None,
        validation_alias=AliasChoices("per-ip-shaper", "per_ip_shaper"),
        serialization_alias="per-ip-shaper",
    )
    permit_any_host: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("permit-any-host", "permit_any_host"),
        serialization_alias="permit-any-host",
    )
    permit_stun_host: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("permit-stun-host", "permit_stun_host"),
        serialization_alias="permit-stun-host",
    )
    policy_behaviour_type: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("policy-behaviour-type", "policy_behaviour_type"),
        serialization_alias="policy-behaviour-type",
    )
    policy_expiry: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("policy-expiry", "policy_expiry"),
        serialization_alias="policy-expiry",
    )
    policy_expiry_date: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("policy-expiry-date", "policy_expiry_date"),
        serialization_alias="policy-expiry-date",
    )
    policy_expiry_date_utc: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("policy-expiry-date-utc", "policy_expiry_date_utc"),
        serialization_alias="policy-expiry-date-utc",
    )
    policyid: Optional[int] = None
    poolname: Optional[List[str]] = None  # TODO: Define the PoolName class and use it here instead of List[str]
    poolname6: Optional[List[str]] = None  # TODO: Define the PoolName6 class and use it here instead of List[str]
    profile_group: Optional[str] = Field(
        # TODO: Define the ProfileGroup class and use it here instead of str
        None,
        validation_alias=AliasChoices("profile-group", "profile_group"),
        serialization_alias="profile-group",
    )
    profile_protocol_options: Optional[List[str]] = Field(
        # TODO: Define the ProtocolOptionsProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("profile-protocol-options", "profile_protocol_options"),
        serialization_alias="profile-protocol-options",
    )
    profile_type: Optional[PROFILE_TYPE] = Field(
        None,
        validation_alias=AliasChoices("profile-type", "profile_type"),
        serialization_alias="profile-type",
    )
    #######
    radius_mac_auth_bypass: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("radius-mac-auth-bypass", "radius_mac_auth_bypass"),
        serialization_alias="radius-mac-auth-bypass",
    )
    redirect_url: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("redirect-url", "redirect_url"),
        serialization_alias="redirect-url",
    )
    replacemsg_override_group: Optional[List[str]] = Field(
        # TODO: Define ReplacemsgOverrideGroup class and use it here instead of str
        None,
        validation_alias=AliasChoices("replacemsg-override-group", "replacemsg_override_group"),
        serialization_alias="replacemsg-override-group",
    )
    reputation_direction: Optional[REPUTATION_DIRECTION_TYPE] = Field(
        None,
        validation_alias=AliasChoices("reputation-direction", "reputation_direction"),
        serialization_alias="reputation-direction",
    )
    reputation_direction6: Optional[REPUTATION_DIRECTION_TYPE] = Field(
        None,
        validation_alias=AliasChoices("reputation-direction6", "reputation_direction6"),
        serialization_alias="reputation-direction6",
    )
    reputation_minimum: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("reputation-minimum", "reputation_minimum"),
        serialization_alias="reputation-minimum",
    )
    reputation_minimum6: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("reputation-minimum6", "reputation_minimum6"),
        serialization_alias="reputation-minimum6",
    )
    rtp_addr: Optional[List[str]] = Field(  # TODO: Define RtpAddr class and use it here instead of List[str]
        None,
        validation_alias=AliasChoices("rtp-addr", "rtp_addr"),
        serialization_alias="rtp-addr",
    )
    rtp_nat: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("rtp-nat", "rtp_nat"),
        serialization_alias="rtp-nat",
    )
    schedule: Optional[List[str]] = None  # TODO: Define Schedule class and use it here instead of str
    schedule_timeout: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("schedule-timeout", "schedule_timeout"),
        serialization_alias="schedule-timeout",
    )
    # TODO: Define SctpFilterProfile class and use it here instead of str
    sctp_filter_profile: Optional[List[str]] = Field(
        None,
        validation_alias=AliasChoices("sctp-filter-profile", "sctp_filter_profile"),
        serialization_alias="sctp-filter-profile",
    )
    send_deny_packet: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("send-deny-packet", "send_deny_packet"),
        serialization_alias="send-deny-packet",
    )
    service: Optional[List[Union[str, ServiceCustom, ServiceGroup]]] = None
    service_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("service-negate", "service_negate"),
        serialization_alias="service-negate",
    )
    ####
    session_ttl: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("session-ttl", "session_ttl"),
        serialization_alias="session-ttl",
    )
    sgt: Optional[List[int]] = None
    sgt_check: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("sgt-check", "sgt_check"),
        serialization_alias="sgt-check",
    )
    # TODO: Define the SrcVendorMac class and use it here instead of List[str]
    src_vendor_mac: Optional[List[str]] = None
    srcaddr: Optional[List[Union[str, Address, AddressGroup]]] = None
    srcaddr_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("srcaddr-negate", "srcaddr_negate"),
        serialization_alias="srcaddr-negate",
    )
    srcaddr6: Optional[List[str]] = None  # TODO: Define the SrcAddr6 class and use it here instead of List[str]
    srcaddr6_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("srcaddr6-negate", "srcaddr6_negate"),
        serialization_alias="srcaddr6-negate",
    )
    srcintf: Optional[List[str]] = None  # TODO: Define the SrcIntf class and use it here instead of List[str]
    ssh_filter_profile: Optional[str] = Field(
        # TODO: Define the SSHFilterProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("ssh-filter-profile", "ssh_filter_profile"),
        serialization_alias="ssh-filter-profile",
    )
    ssh_policy_redirect: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("ssh-policy-redirect", "ssh_policy_redirect"),
        serialization_alias="ssh-policy-redirect",
    )
    ssl_ssh_profile: Optional[List[str]] = Field(
        # TODO: Define the SSLSSHProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("ssl-ssh-profile", "ssl_ssh_profile"),
        serialization_alias="ssl-ssh-profile",
    )
    status: Optional[ENABLE_DISABLE] = None
    tcp_mss_receiver: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("tcp-mss-receiver", "tcp_mss_receiver"),
        serialization_alias="tcp-mss-receiver",
    )
    tcp_mss_sender: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("tcp-mss-sender", "tcp_mss_sender"),
        serialization_alias="tcp-mss-sender",
    )
    tcp_session_without_syn: Optional[TCP_SESSION_WO_SYN_TYPE] = Field(
        None,
        validation_alias=AliasChoices("tcp-session-without-syn", "tcp_session_without_syn"),
        serialization_alias="tcp-session-without-syn",
    )
    timeout_send_rst: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("timeout-send-rst", "timeout_send_rst"),
        serialization_alias="timeout-send-rst",
    )
    tos: Optional[str] = None
    tos_mask: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("tos-mask", "tos_mask"),
        serialization_alias="tos-mask",
    )
    tos_negate: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("tos-negate", "tos_negate"),
        serialization_alias="tos-negate",
    )
    traffic_shaper: Optional[List[str]] = Field(
        # TODO: Define the TrafficShaper class and use it here instead of str
        None,
        validation_alias=AliasChoices("traffic-shaper", "traffic_shaper"),
        serialization_alias="traffic-shaper",
    )
    traffic_shaper_reverse: Optional[List[str]] = Field(
        # TODO: Define the TrafficShaperReverse class and use it here instead of str
        None,
        validation_alias=AliasChoices("traffic-shaper-reverse", "traffic_shaper_reverse"),
        serialization_alias="traffic-shaper-reverse",
    )
    users: Optional[List[str]] = None  # TODO: Define the Users class and use it here instead of List[str]
    utm_status: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("utm-status", "utm_status"),
        serialization_alias="utm-status",
    )
    uuid: Optional[str] = None
    videofilter_profile: Optional[List[str]] = Field(
        # TODO: Define the VideoFilterProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("videofilter-profile", "videofilter_profile"),
        serialization_alias="videofilter-profile",
    )
    virtual_patch_profile: Optional[str] = Field(
        # TODO: Define the VirtualPatchProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("virtual-patch-profile", "virtual_patch_profile"),
        serialization_alias="virtual-patch-profile",
    )
    vlan_cos_fwd: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("vlan-cos-fwd", "vlan_cos_fwd"),
        serialization_alias="vlan-cos-fwd",
    )
    vlan_cos_rev: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("vlan-cos-rev", "vlan_cos_rev"),
        serialization_alias="vlan-cos-rev",
    )
    vlan_filter: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("vlan-filter", "vlan_filter"),
        serialization_alias="vlan-filter",
    )
    voip_profile: Optional[Union[str, list]] = Field(
        # TODO: Define the VoipProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("voip-profile", "voip_profile"),
        serialization_alias="voip-profile",
    )
    vpntunnel: Optional[str] = None  # TODO: Define the VpnTunnel class and use it here instead of str
    waf_profile: Optional[str] = Field(
        # TODO: Define the WafProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("waf-profile", "waf_profile"),
        serialization_alias="waf-profile",
    )
    wccp: Optional[ENABLE_DISABLE] = None
    webfilter_profile: Optional[List[str]] = Field(
        # TODO: Define the WebFilterProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("webfilter-profile", "webfilter_profile"),
        serialization_alias="webfilter-profile",
    )
    webproxy_forward_server: Optional[str] = Field(
        # TODO: Define the WebProxyForwardServer class and use it here instead of str
        None,
        validation_alias=AliasChoices("webproxy-forward-server", "webproxy_forward_server"),
        serialization_alias="webproxy-forward-server",
    )
    webproxy_profile: Optional[str] = Field(
        # TODO: Define the WebProxyProfile class and use it here instead of str
        None,
        validation_alias=AliasChoices("webproxy-profile", "webproxy_profile"),
        serialization_alias="webproxy-profile",
    )
    ztna_device_ownership: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("ztna-device-ownership", "ztna_device_ownership"),
        serialization_alias="ztna-device-ownership",
    )
    ztna_ems_tag: Optional[List[str]] = Field(
        # TODO: Define the ZtnaEmsTag class and use it here instead of List[str]
        None,
        validation_alias=AliasChoices("ztna-ems-tag", "ztna_ems_tag"),
        serialization_alias="ztna-ems-tag",
    )
    ztna_ems_tag_secondary: Optional[List[str]] = Field(
        # TODO: Define the ZtnaEmsTag class and use it here instead of List[str]
        None,
        validation_alias=AliasChoices("ztna-ems-tag-secondary", "ztna_ems_tag_secondary"),
        serialization_alias="ztna-ems-tag-secondary",
    )
    ztna_geo_tag: Optional[List[str]] = Field(
        # TODO: Define the ZtnaGeoTag class and use it here instead of List[str]
        None,
        validation_alias=AliasChoices("ztna-geo-tag", "ztna_geo_tag"),
        serialization_alias="ztna-geo-tag",
    )
    ztna_policy_redirect: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("ztna-policy-redirect", "ztna_policy_redirect"),
        serialization_alias="ztna-policy-redirect",
    )
    ztna_status: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("ztna-status", "ztna_status"),
        serialization_alias="ztna-status",
    )
    ztna_tags_match_logic: Optional[OR_AND] = Field(
        None,
        validation_alias=AliasChoices("ztna-tags-match-logic", "ztna_tags_match_logic"),
        serialization_alias="ztna-tags-match-logic",
    )

    @property
    def get_url(self) -> str:
        """Construct API URL based on adom and pkg fields

        Notes:
            ADOM can come from FMG object
            PKG must be specified
        """
        adom = self.adom or self.fmg_scope.replace("adom/", "").replace("global", "")
        pkg = self.pkg
        if not adom:
            raise ValueError("Please specify `adom` field or assign object to FMG!")
        if pkg is None:
            raise ValueError("Please specify `pkg` field!")
        return self._url.replace("{adom}", adom).replace("{pkg}", pkg)

    @field_validator(
        "anti_replay",
        "auth_path",
        "block_notification",
        "captive_portal_exempt",
        "capture_packet",
        "delay_tcp_npu_session",
        "diffserv_copy",
        "diffserv_forward",
        "diffserv_reverse",
        "dsri",
        "dstaddr_negate",
        "dstaddr6_negate",
        "dynamic_shaping",
        "email_collect",
        "fec",
        "fixedport",
        "geoip_anycast",
        "http_policy_redirect",
        "inbound",
        "internet_service",
        "internet_service_negate",
        "internet_service_src",
        "internet_service_src_negate",
        "internet_service6",
        "internet_service6_negate",
        "internet_service6_src",
        "internet_service6_src_negate",
        "ippool",
        "logtraffic_start",
        "match_vip",
        "match_vip_only",
        "nat",
        "nat46",
        "nat64",
        "natinbound",
        "natoutbound",
        "ntlm",
        "ntlm_guest",
        "outbound",
        "passive_wan_health_measurement",
        "pcp_inbound",
        "pcp_outbound",
        "permit_any_host",
        "permit_stun_host",
        "policy_expiry",
        "radius_mac_auth_bypass",
        "rtp_nat",
        "schedule_timeout",
        "send_deny_packet",
        "service_negate",
        "sgt_check",
        "srcaddr_negate",
        "srcaddr6_negate",
        "ssh_policy_redirect",
        "status",
        "timeout_send_rst",
        "tos_negate",
        "utm_status",
        "wccp",
        "ztna_device_ownership",
        "ztna_policy_redirect",
        "ztna_status",
        mode="before",
    )
    def standardize_enabled_disabled(cls, v):
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_serializer("srcaddr", "dstaddr", "service")
    def member_names_only(self, members: List[Union[str, Address, AddressGroup, ServiceCustom, ServiceGroup]]) -> List[str]:
        """Ensure member names are passed to API as it is expected"""
        serialized = []
        for member in members:
            if isinstance(member, str):
                serialized.append(member)
                continue
            serialized.append(member.name)
        return serialized