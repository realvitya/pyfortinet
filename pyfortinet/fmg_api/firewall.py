"""Firewall object types"""

from ipaddress import IPv4Interface, IPv4Address
from typing import Literal, Optional, Union, List
from uuid import UUID

from more_itertools import first
from pydantic import Field, field_validator, AliasChoices, BaseModel, field_serializer

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import Scope

ADDRESS_GROUP_TYPE = Literal["default", "array", "folder"]
ADDRESS_GROUP_CATEGORY = Literal["default", "ztna-ems-tag", "ztna-geo-tag"]
ENABLE_DISABLE = Literal["disable", "enable"]
ADDRESS_TYPE = Literal[
    "ipmask",
    "iprange",
    "fqdn",
    "wildcard",
    "geography",
    "url",
    "wildcard-fqdn",
    "nsx",
    "aws",
    "dynamic",
    "interface-subnet",
    "mac",
    "fqdn-group",
]
CLEARPASS_SPT = Literal["unknown", "healthy", "quarantine", "checkup", "transition", "infected", "transient"]
DIRTY = Literal["dirty", "clean"]
OBJ_TYPE = Literal["ip", "mac"]
SDN_ADDR_TYPE = Literal["private", "public", "all"]
SUB_TYPE = Literal[
    "sdn", "clearpass-spt", "fsso", "ems-tag", "swc-tag", "fortivoice-tag", "fortinac-tag", "fortipolicy-tag"
]
APP_SERVICE_TYPE = Literal["disable", "app-id", "app-category"]
CHECK_RESET_RANGE = Literal["disable", "default", "strict"]
HELPER = Literal[
    "disable",
    "auto",
    "ftp",
    "tftp",
    "ras",
    "h323",
    "tns",
    "mms",
    "sip",
    "pptp",
    "rtsp",
    "dns-udp",
    "dns-tcp",
    "pmap",
    "rsh",
    "dcerpc",
    "mgcp",
    "gtp-c",
    "gtp-u",
    "gtp-b",
    "pfcp",
]
PROTOCOL = Literal[
    "ICMP", "IP", "TCP/UDP/SCTP", "ICMP6", "HTTP", "FTP", "CONNECT", "SOCKS", "ALL", "SOCKS-TCP", "SOCKS-UDP"
]


class AddressTagging(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    tags: Optional[List[str]] = None


class Address(FMGObject):
    """Address class for high-level operations

    Attributes:
        name (str): object name
        allow_routing (str): Defines whether the use of this address in the static route configuration
                             is enabled or disabled, with possible values being 'disable' or 'enable'.
        associated_interface (str|list[str]): object assigned to interface/zone name
        subnet (str|list[str]): subnet in x.x.x.x/x or [x.x.x.x, y.y.y.y] format
        cache_ttl (int): Defines the minimal TTL (Time To Live) of individual IP addresses in FQDN
                         cache measured in seconds.
        clearpass_spt (str): Represents the SPT (System Posture Token) value, indicating system status.
                             Possible values include 'healthy', 'quarantine', 'transition', etc.
        color (int): color code for the address object icon on the GUI.
        comment (str): comment for the address object.
        country (str): IP addresses associated to a specific country.
        dirty (str): Indicates whether the address is to be deleted; possible values 'dirty' or 'clean'.
        end_ip (str): The final IP address (inclusive) in the range for the address.
        epg_name (str): endpoint group name.
        fabric_object (str): Indicates the Security Fabric global object setting,
                             with possible values being 'disable' or 'enable'.
        filter (str): Match criteria filter.
        fqdn (str): Fully Qualified Domain Name address.
        fsso_group (List[str]): A list of FSSO group(s).
        interface (str): Name of interface whose IP address is to be used.
        list (List[AddressList]): List (TODO: figure out, docs don't help)
        macaddr (List[str]): Multiple MAC address ranges.
        node_ip_only (str): Defines whether only the collection of node addresses in Kubernetes
                            is enabled or disabled. Possible values are 'disable' or 'enable'.
        obj_id (str): Object ID for NSX.
        obj_tag (str): Tag of dynamic address object.
        obj_type (str): type of the object (IP, MAC)
        organization (str): Organization domain name (Syntax: organization/domain).
        policy_group (str): policy group name.
        sdn (str): SDN.
        sdn_addr_type (str): Type of addresses to collect.
        sdn_tag (str): SDN tag.
        start_ip (str): First IP address (inclusive) in the range for the address.
        sub_type (str): Indicates the sub-type of address.
                        Possible values include 'sdn', 'clearpass-spt', 'fsso', etc.
        subnet_name (str): Subnet name.
        tag_detection_level (str): Tag detection level of dynamic address object.
        tag_type (str): Tag type of dynamic address object.
        tagging (List[AddressTagging]): tagging details for this address.
        tenant (str): tenant related to this address.
        type (str): Indicates the type of address. Possible values include 'ipmask', 'iprange', 'fqdn', etc.
        uuid (str): Contains the Universally Unique Identifier (UUID; automatically assigned but can be manually reset).
        wildcard (str): This is the IP address and wildcard netmask.
        wildcard_fqdn (str): Contains a Fully Qualified Domain Name with wildcard characters.
        global_object (int): global object related to this address.
        mapping__scope (List[dict, Scope]): the mapping scope for this address.
    """

    class AddressList(BaseModel):
        ip: Optional[str] = None
        net_id: Optional[str] = Field(
            None, validation_alias=AliasChoices("net-id", "net_id"), serialization_alias="net-id"
        )
        obj_id: Optional[str] = Field(
            None, validation_alias=AliasChoices("obj-id", "obj_id"), serialization_alias="obj-id"
        )

    _url: str = "/pm/config/{scope}/obj/firewall/address"
    _master_keys: list = ["name"]
    name: Optional[str] = Field(None, max_length=128)
    allow_routing: Optional[ENABLE_DISABLE] = Field(
        None, validation_alias=AliasChoices("allow-routing", "allow_routing"), serialization_alias="allow-routing"
    )
    associated_interface: Optional[Union[str, list[str]]] = Field(
        None,
        validation_alias=AliasChoices("associated-interface", "associated_interface"),
        serialization_alias="associated-interface",
    )
    cache_ttl: Optional[int] = Field(
        None, validation_alias=AliasChoices("cache-ttl", "cache_ttl"), serialization_alias="cache-ttl"
    )
    clearpass_spt: Optional[CLEARPASS_SPT] = Field(
        None, validation_alias=AliasChoices("clearpass-spt", "clearpass_spt"), serialization_alias="clearpass-spt"
    )
    color: Optional[int] = None
    comment: Optional[str] = None
    country: Optional[str] = None
    dirty: Optional[DIRTY] = None
    dynamic_mapping: Optional[Union[List["Address"], "Address"]] = None
    end_ip: Optional[str] = None
    epg_name: Optional[str] = Field(
        None, validation_alias=AliasChoices("epg-name", "epg_name"), serialization_alias="epg-name"
    )
    fabric_object: Optional[ENABLE_DISABLE] = Field(
        None, validation_alias=AliasChoices("fabric-object", "fabric_object"), serialization_alias="fabric-object"
    )
    filter: Optional[str] = None
    fqdn: Optional[str] = None
    fsso_group: Optional[List[str]] = Field(
        None, validation_alias=AliasChoices("fsso-group", "fsso_group"), serialization_alias="fsso-group"
    )
    interface: Optional[str] = None
    list: Optional[List["AddressList"]] = None
    macaddr: Optional[List[str]] = None
    node_ip_only: Optional[ENABLE_DISABLE] = Field(
        None, validation_alias=AliasChoices("node-ip-only", "node_ip_only"), serialization_alias="node-ip-only"
    )
    obj_id: Optional[str] = Field(None, validation_alias=AliasChoices("obj-id", "obj_id"), serialization_alias="obj-id")
    obj_tag: Optional[str] = Field(
        None, validation_alias=AliasChoices("obj-tag", "obj_tag"), serialization_alias="obj-tag"
    )
    obj_type: Optional[OBJ_TYPE] = Field(
        None, validation_alias=AliasChoices("obj-type", "obj_type"), serialization_alias="obj-type"
    )
    organization: Optional[str] = None
    policy_group: Optional[str] = Field(
        None, validation_alias=AliasChoices("policy-group", "policy_group"), serialization_alias="policy-group"
    )
    sdn: Optional[str] = None
    sdn_addr_type: Optional[SDN_ADDR_TYPE] = Field(
        None, validation_alias=AliasChoices("sdn-addr-type", "sdn_addr_type"), serialization_alias="sdn-addr-type"
    )
    sdn_tag: Optional[str] = Field(
        None, validation_alias=AliasChoices("sdn-tag", "sdn_tag"), serialization_alias="sdn-tag"
    )
    start_ip: Optional[str] = Field(
        None, validation_alias=AliasChoices("start-ip", "start_ip"), serialization_alias="start-ip"
    )
    sub_type: Optional[SUB_TYPE] = Field(
        None, validation_alias=AliasChoices("sub-type", "sub_type"), serialization_alias="sub-type"
    )
    subnet: Optional[Union[str, List[str]]] = None
    subnet_name: Optional[str] = Field(
        None, validation_alias=AliasChoices("subnet-name", "subnet_name"), serialization_alias="subnet-name"
    )
    tag_detection_level: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("tag-detection-level", "tag_detection_level"),
        serialization_alias="tag-detection-level",
    )
    tag_type: Optional[str] = Field(
        None, validation_alias=AliasChoices("tag-type", "tag_type"), serialization_alias="tag-type"
    )
    tagging: Optional[List[AddressTagging]] = None
    tenant: Optional[str] = None
    type: Optional[ADDRESS_TYPE] = None
    uuid: Optional[str] = None
    wildcard: Optional[str] = None
    wildcard_fqdn: Optional[str] = Field(
        None, validation_alias=AliasChoices("wildcard-fqdn", "wildcard_fqdn"), serialization_alias="wildcard-fqdn"
    )
    # Mapping fields
    global_object: Optional[int] = Field(
        None, validation_alias=AliasChoices("global-object", "global_object"), serialization_alias="global-object"
    )
    mapping__scope: Optional[Union[Union[dict, Scope], List[Union[dict, Scope]]]] = Field(
        None, validation_alias=AliasChoices("_scope", "mapping__scope"), serialization_alias="_scope"
    )

    @field_validator("subnet")
    def standardize_subnet(cls, v):
        """validator: x.x.x.x/y.y.y.y -> x.x.x.x/y

        API use this list form: ["1.2.3.4", "255.255.255.0"]
        Human use this form: "1.2.3.4/24"
        """
        if isinstance(v, list):
            return IPv4Interface("/".join(v)).compressed
        else:
            return IPv4Interface(v).compressed

    @field_validator("associated_interface")
    def standardize_assoc_iface(cls, v):
        """validator: FMG sends a list with a single element, replace with single element"""
        if isinstance(v, list):
            return first(v, None)
        else:
            return v

    @field_validator("allow_routing", mode="before")
    def validate_allow_routing(cls, v) -> ENABLE_DISABLE:
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("type", mode="before")
    def validate_type(cls, v) -> ADDRESS_TYPE:
        return ADDRESS_TYPE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("clearpass_spt", mode="before")
    def validate_clearpass_spt(cls, v) -> CLEARPASS_SPT:
        return CLEARPASS_SPT.__dict__.get("__args__")[v] if isinstance(v, int) else v

    # @field_validator("dirty", mode="before")
    # def validate_dirty(cls, v: int) -> DIRTY:
    #     return DIRTY.__dict__.get("__args__")[v] if isinstance(v, int) else v
    # got value 2=dirty!

    @field_validator("end_ip", mode="before")
    def validate_end_ip(cls, v: str) -> str:
        assert IPv4Address(v)
        return v

    @field_validator("fabric_object", mode="before")
    def validate_fabric_object(cls, v) -> str:
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("node_ip_only", mode="before")
    def validate_node_ip_only(cls, v) -> str:
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    # @field_validator("obj_type", mode="before")
    # def validate_obj_type(cls, v: int) -> str:
    #     return OBJ_TYPE.__dict__.get("__args__")[v] if isinstance(v, int) else v
    # got value 7=ip!

    @field_validator("sdn_addr_type", mode="before")
    def validate_sdn_addr_type(cls, v) -> str:
        return SDN_ADDR_TYPE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("start_ip", mode="before")
    def validate_start_ip(cls, v: str) -> str:
        assert IPv4Address(v)
        return v

    @field_validator("sub_type", mode="before")
    def validate_sub_type(cls, v) -> str:
        return SUB_TYPE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("wildcard", mode="before")
    def validate_wildcard(cls, v) -> str:
        """Ensure wildcard address definition is correct (x.x.x.x y.y.y.y)"""
        if isinstance(v, list):
            return " ".join(IPv4Address(part).compressed for part in v)
        else:  # string
            return " ".join(IPv4Address(part).compressed for part in v.split())

    @field_validator("uuid", mode="before")
    def validate_uuid(cls, v) -> str:
        assert UUID(v)
        return str(v)


class AddressGroup(FMGObject):
    _url: str = "/pm/config/{scope}/obj/firewall/addrgrp"
    _master_keys: list = ["name"]
    allow_routing: Optional[ENABLE_DISABLE] = Field(
        None, validation_alias=AliasChoices("allow-routing", "allow_routing"), serialization_alias="allow-routing"
    )
    category: Optional[ADDRESS_GROUP_CATEGORY] = "default"
    color: Optional[int] = None
    comment: Optional[str] = None
    dynamic_mapping: Optional[Union[List["AddressGroup"], "AddressGroup"]] = None
    exclude: Optional[ENABLE_DISABLE] = None
    exclude_member: Optional[List[Union[str, Address, "AddressGroup"]]] = Field(
        None,
        max_length=5000,
        validation_alias=AliasChoices("exclude-member", "exclude_member"),
        serialization_alias="exclude-member",
    )
    fabric_object: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fabric-object", "fabric_object"),
        serialization_alias="fabric-object",
    )
    member: Optional[List[Union[str, Address, "AddressGroup"]]] = Field(None, max_length=5000)
    name: Optional[str] = None
    tagging: Optional[List[AddressTagging]] = None
    type: Optional[ADDRESS_GROUP_TYPE] = "default"
    uuid: Optional[str] = None

    @field_serializer("member", "exclude_member")
    def member_names_only(members: List[Union[str, Address, "AddressGroup"]]) -> List[str]:
        """Ensure member names are passed to API as it is expected"""
        serialized = []
        for member in members:
            if isinstance(member, str):
                serialized.append(member)
                continue
            serialized.append(member.name)
        return serialized

    @field_validator("category", mode="before")
    def validate_category(cls, v) -> ADDRESS_GROUP_CATEGORY:
        return ADDRESS_GROUP_CATEGORY.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("allow_routing", "exclude", "fabric_object", mode="before")
    def validate_enable_disable(cls, v) -> ENABLE_DISABLE:
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("type", mode="before")
    def validate_type(cls, v) -> ADDRESS_GROUP_TYPE:
        return ADDRESS_GROUP_TYPE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("uuid", mode="before")
    def validate_uuid(cls, v) -> str:
        assert UUID(v)
        return str(v)


class ServiceCategory(FMGObject):
    _url = "/pm/config/{scope}/firewall/service/category"
    _master_keys = ["name"]
    comment: Optional[str] = None
    fabric_object: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fabric-object", "fabric_object"),
        serialization_alias="fabric-object",
    )
    name: Optional[str] = None

    @field_validator("fabric_object", mode="before")
    def standardize_enabled_disabled(cls, v):
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v


class ServiceCustom(FMGObject):
    """Custom service class

    Attributes:
        app_category
        app_service_type
        application
        category
        check_reset_range
        color
        comment
        fabric_object
        fqdn
        helper
        icmpcode
        icmptype
        iprange
        name
        protocol
        protocol_number
        proxy
        sctp_portrange
        session_ttl
        tcp_halfclose_timer
        tcp_halfopen_timer
        tcp_portrange
        tcp_rst_timer
        tcp_timewait_timer
        udp_idle_timer
        udp_portrange
        visibility
    """
    _url = "/pm/config/{scope}/firewall/service/custom"
    _master_keys = ["name"]
    app_category: Optional[List[int]] = Field(
        None,
        validation_alias=AliasChoices("app-category", "app_category"),
        serialization_alias="app-category",
    )
    app_service_type: Optional[APP_SERVICE_TYPE] = Field(
        None,
        validation_alias=AliasChoices("app-service-type", "app_service_type"),
        serialization_alias="app-service-type",
    )
    application: Optional[int] = None
    category: Optional[ServiceCategory] = None
    check_reset_range: Optional[CHECK_RESET_RANGE] = Field(
        None,
        validation_alias=AliasChoices("check-reset-range", "check_reset_range"),
        serialization_alias="check-reset-range",
    )
    color: Optional[int] = None
    comment: Optional[str] = None
    fabric_object: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fabric-object", "fabric_object"),
        serialization_alias="fabric-object",
    )
    fqdn: Optional[str] = None
    helper: Optional[HELPER] = None
    icmpcode: Optional[int] = None
    icmptype: Optional[int] = None
    iprange: Optional[str] = None
    name: Optional[str] = None
    protocol: Optional[PROTOCOL] = None
    protocol_number: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("protocol-number", "protocol_number"),
        serialization_alias="protocol-number",
    )
    proxy: Optional[ENABLE_DISABLE] = None
    sctp_portrange: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("sctp-portrange", "sctp_portrange"),
        serialization_alias="sctp-portrange",
    )
    session_ttl: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("session-ttl", "session_ttl"),
        serialization_alias="session-ttl",
    )
    tcp_halfclose_timer: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("tcp-halfclose-timer", "tcp_halfclose_timer"),
        serialization_alias="tcp-halfclose-timer",
    )
    tcp_halfopen_timer: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("tcp-halfopen-timer", "tcp_halfopen_timer"),
        serialization_alias="tcp-halfopen-timer",
    )
    tcp_portrange: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("tcp-portrange", "tcp_portrange"),
        serialization_alias="tcp-portrange",
    )
    tcp_rst_timer: Optional[int] = Field(
        None, validation_alias=AliasChoices("tcp-rst-timer", "tcp_rst_timer"), serialization_alias="tcp-rst-timer"
    )
    tcp_timewait_timer: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("tcp-timewait-timer", "tcp_timewait_timer"),
        serialization_alias="tcp-timewait-timer",
    )
    udp_idle_timer: Optional[int] = Field(
        None, validation_alias=AliasChoices("udp-idle-timer", "udp_idle_timer"), serialization_alias="udp-idle-timer"
    )
    udp_portrange: Optional[str] = Field(
        None, validation_alias=AliasChoices("udp-portrange", "udp_portrange"), serialization_alias="udp-portrange"
    )
    visibility: Optional[ENABLE_DISABLE] = None

    @field_validator("app_service_type", mode="before")
    def standardize_app_service_type(cls, v):
        return APP_SERVICE_TYPE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("check_reset_range", mode="before")
    def standardize_check_reset_range(cls, v):
        return CHECK_RESET_RANGE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("fabric_object", "proxy", "visibility", mode="before")
    def standardize_enabled_disabled(cls, v):
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("helper", mode="before")
    def standardize_helper(cls, v):
        return HELPER.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("protocol", mode="before")
    def standardize_protocol(cls, v):
        return PROTOCOL.__dict__.get("__args__")[v] if isinstance(v, int) else v


class ServiceGroup(FMGObject):
    """Service group class

    Attributes:

    """
    _url = "/pm/config/{scope}/firewall/service/group"
    _master_keys = ["name"]
    color: Optional[int] = None
    comment: Optional[str] = None
    fabric_object: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fabric-object", "fabric_object"),
        serialization_alias="fabric-object",
    )
    member: Optional[List[Union[str, ServiceCustom]]] = Field(None, max_length=5000)
    name: Optional[str] = None
    proxy: Optional[ENABLE_DISABLE] = None

    @field_serializer("member")
    def member_names_only(members: List[Union[str, Address, "AddressGroup"]]) -> List[str]:
        """Ensure member names are passed to API as it is expected"""
        serialized = []
        for member in members:
            if isinstance(member, str):
                serialized.append(member)
                continue
            serialized.append(member.name)
        return serialized

    @field_validator("fabric_object", "proxy", mode="before")
    def standardize_enabled_disabled(cls, v):
        return ENABLE_DISABLE.__dict__.get("__args__")[v] if isinstance(v, int) else v


class ProfileGroup(FMGObject):
    """Service group class

    Attributes:
        application_list: Name of an existing Application list.
        av_profile: Name of an existing Antivirus profile.
        dlp_profile: Name of an existing DLP profile.
        dnsfilter_profile: Name of an existing DNS filter profile.
        emailfilter_profile: Name of an existing email filter profile.
        file_filter_profile: Name of an existing file_filter profile.
        icap_profile: Name of an existing ICAP profile.
        ips_sensor: Name of an existing IPS sensor.
        ips_voip_filter: Name of an existing VoIP (ips) profile.
        name: Profile group name.
        profile_protocol_options: Name of an existing Protocol options profile.
        sctp_filter_profile: Name of an existing SCTP filter profile.
        ssh_filter_profile: Name of an existing SSH filter profile.
        ssl_ssh_profile: Name of an existing SSL SSH profile.
        videofilter_profile: Name of an existing VideoFilter profile.
        voip_profile: Name of an existing VoIP (voipd) profile.
        waf_profile: Name of an existing Web application firewall profile.
        webfilter_profile: Name of an existing Web filter profile.
    """
    _url = "/pm/config/{scope}/obj/firewall/profile-group"
    _master_keys = ["name"]
    application_list: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("application-list", "application_list"),
        serialization_alias="application-list"
    )
    av_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("av-profile", "av_profile"),
        serialization_alias="av-profile"
    )
    dlp_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dlp-profile", "dlp_profile"),
        serialization_alias="dlp-profile"
    )
    dnsfilter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("dnsfilter-profile", "dnsfilter_profile"),
        serialization_alias="dnsfilter-profile"
    )
    emailfilter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("emailfilter-profile", "emailfilter_profile"),
        serialization_alias="emailfilter-profile"
    )
    file_filter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("file-filter-profile", "file_filter_profile"),
        serialization_alias="file-filter-profile"
    )
    icap_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("icap-profile", "icap_profile"),
        serialization_alias="icap-profile"
    )
    ips_sensor: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ips-sensor", "ips_sensor"),
        serialization_alias="ips-sensor"
    )
    ips_voip_filter: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ips-voip-filter", "ips_voip_filter"),
        serialization_alias="ips-voip-filter"
    )
    name: Optional[str] = None
    profile_protocol_options: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("profile-protocol-options", "profile_protocol_options"),
        serialization_alias="profile-protocol-options"
    )
    sctp_filter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("sctp-filter-profile", "sctp_filter_profile"),
        serialization_alias="sctp-filter-profile"
    )
    ssh_filter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ssh-filter-profile", "ssh_filter_profile"),
        serialization_alias="ssh-filter-profile"
    )
    ssl_ssh_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ssl-ssh-profile", "ssl_ssh_profile"),
        serialization_alias="ssl-ssh-profile"
    )
    videofilter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("videofilter-profile", "videofilter_profile"),
        serialization_alias="videofilter-profile"
    )
    voip_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("voip-profile", "voip_profile"),
        serialization_alias="voip-profile"
    )
    waf_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("waf-profile", "waf_profile"),
        serialization_alias="waf-profile"
    )
    webfilter_profile: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("webfilter-profile", "webfilter_profile"),
        serialization_alias="webfilter-profile"
    )
