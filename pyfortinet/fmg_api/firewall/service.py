"""Custom firewall services, port ranges, and service groups."""

import re
from typing import Optional, Union

from pydantic import AliasChoices, BaseModel, Field, field_serializer, field_validator, model_validator
from typing_extensions import Self

from pyfortinet.fmg_api import FMGObject

from .types import APP_SERVICE_TYPE, CHECK_RESET_RANGE, ENABLE_DISABLE, HELPER, PROTOCOL


class ServiceCategory(FMGObject):
    _url = "/pm/config/{scope}/obj/firewall/service/category/{category}"
    _master_keys = {"category": "name"}
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


class PortRange(BaseModel):
    """Port range class

    This dataclass is to hold source_start:source_end and destination_start:destination_end port data.
    For a single source or destination port, either the start or end endpoint can be supplied.
    The missing endpoint is normalized to the supplied value.
    """

    source_start: Optional[str] = None
    source_end: Optional[str] = None
    destination_start: Optional[str] = None
    destination_end: Optional[str] = None

    @model_validator(mode="after")
    def standardize_port_handling(self) -> Self:
        """Ensure start and end are either None or the same if not different"""
        try:
            if int(self.source_start) > int(self.source_end):
                raise ValueError("Start port must be equal or less than end port!")
        except TypeError:
            pass
        try:
            if int(self.destination_start) > int(self.destination_end):
                raise ValueError("Start port must be equal or less than end port!")
        except TypeError:
            pass

        self.source_start = self.source_start or self.source_end
        self.source_end = self.source_end or self.source_start
        self.destination_start = self.destination_start or self.destination_end
        self.destination_end = self.destination_end or self.destination_start
        return self


PORT_RANGE_TYPE = Union[Union[str, PortRange], list[Union[str, PortRange]]]


class ServiceCustom(FMGObject):
    """Custom service class

    Attributes:
        app_category: Application category ID
        app_service_type: Application service type
        application: Application name ID
        category: Service category
        check_reset_range: Enable to reset session if service does not match
        color: Color of icon on the GUI
        comment: Comment
        fabric_object: Security Fabric global object setting
        fqdn: Fully Qualified Domain Name (FQDN)
        helper: Name of helper
        icmpcode: ICMP code
        icmptype: ICMP type
        iprange: Start and end IP addresses for the range
        name: Service name
        protocol: Protocol type: TCP/UDP/SCTP/ICMP/ICMP6
        protocol_number: IP protocol number
        proxy: Enable to use this service for proxy
        sctp_portrange: SCTP port range
        session_ttl: Session TTL (Timeout) in seconds
        tcp_halfclose_timer: TCP half-close timer, in seconds
        tcp_halfopen_timer: TCP half-open timer, in seconds
        tcp_portrange: TCP port range
        tcp_rst_timer: TCP RST timer, in seconds
        tcp_timewait_timer: TCP time-wait timer, in seconds
        udp_idle_timer: UDP idle timer, in seconds
        udp_portrange: UDP port range
        visibility: Enable/disable visibility on FortiGate GUI
    """

    _url = "/pm/config/{scope}/obj/firewall/service/custom/{custom}"
    _master_keys = {"custom": "name"}
    app_category: Optional[list[int]] = Field(
        None,
        validation_alias=AliasChoices("app-category", "app_category"),
        serialization_alias="app-category",
    )
    app_service_type: Optional[APP_SERVICE_TYPE] = Field(
        None,
        validation_alias=AliasChoices("app-service-type", "app_service_type"),
        serialization_alias="app-service-type",
    )
    application: Optional[list[int]] = None
    category: Optional[list[Union[ServiceCategory, str]]] = None
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
    sctp_portrange: Optional[PORT_RANGE_TYPE] = Field(
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
    tcp_portrange: Optional[PORT_RANGE_TYPE] = Field(
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
    udp_portrange: Optional[PORT_RANGE_TYPE] = Field(
        None, validation_alias=AliasChoices("udp-portrange", "udp_portrange"), serialization_alias="udp-portrange"
    )
    visibility: Optional[ENABLE_DISABLE] = None

    @field_serializer("category", when_used="unless-none")
    def member_names_only(self, categories: list[Union[str, ServiceCategory]]) -> list[str]:
        """Ensure member names are passed to API as it is expected"""
        serialized = []
        if not categories:
            return []
        for category in categories:
            if isinstance(category, str):
                serialized.append(category)
                continue
            serialized.append(category.name)
        return serialized

    @field_serializer("udp_portrange", "tcp_portrange", "sctp_portrange", when_used="unless-none")
    def portranges_to_string(ranges: list[PortRange]) -> list[str]:
        """Ensure portranges are passed to API as it is expected

            input format is string as follows:
            [dst_start-]dst_end:[src_start-]src_end

        Examples:
            513:512-1023 means: dst 500 and source range of 512-1023
        """
        serialized = []
        if not ranges:
            return []
        for rng in ranges:
            src = ""
            dst = ""

            if rng.source_start and rng.source_start == rng.source_end:
                src = rng.source_start
            elif rng.source_end:
                src = f"{rng.source_start}-{rng.source_end}" if rng.source_start else rng.source_end
            if rng.destination_start and rng.destination_start == rng.destination_end:
                dst = rng.destination_start
            elif rng.destination_end:
                dst = f"{rng.destination_start}-{rng.destination_end}" if rng.destination_start else rng.destination_end
            if src:
                serialized.append(f"{dst}:{src}")
            else:
                serialized.append(dst)
        return serialized

    @field_validator("udp_portrange", "tcp_portrange", "sctp_portrange", mode="plain")
    def ensure_port_ranges(cls, v) -> Optional[list[PortRange]]:
        """Create PortRange object from string to standardize portrange handling"""
        if v is None:
            return None
        ranges = []
        if not isinstance(v, list):
            v = [v]
        for rng in v:
            if isinstance(rng, PortRange):
                ranges.append(rng)
                continue
            if not isinstance(rng, str):
                raise ValueError("Port ranges must be strings or PortRange objects")
            # assuming string
            # format: "dst_st-dst_end:src_st-src_end"
            match = re.fullmatch(
                r"^(?P<dst>(?P<destination_start>\d+)(?:-(?P<destination_end>\d+))?)"
                r"(?::(?P<src>(?P<source_start>\d+)(?:-(?P<source_end>\d+))?))?$",
                rng,
            )
            if not match:
                raise ValueError(f"Invalid port range: {rng!r}")
            data = match.groupdict()
            if not data["destination_end"]:
                data["destination_end"] = data["destination_start"]
            if not data["source_end"]:
                data["source_end"] = data["source_start"]
            ranges.append(PortRange(**data))
        return ranges

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

    _url = "/pm/config/{scope}/obj/firewall/service/group/{group}"
    _master_keys = {"group": "name"}
    color: Optional[int] = None
    comment: Optional[str] = None
    fabric_object: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fabric-object", "fabric_object"),
        serialization_alias="fabric-object",
    )
    member: Optional[list[Union[str, ServiceCustom, "ServiceGroup"]]] = Field(None, max_length=5000)
    name: Optional[str] = None
    proxy: Optional[ENABLE_DISABLE] = None

    @field_serializer("member", when_used="unless-none")
    def member_names_only(self, members: list[Union[str, ServiceCustom, "ServiceGroup"]]) -> list[str]:
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
