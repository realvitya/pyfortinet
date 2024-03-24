"""Firewall object types"""

from ipaddress import IPv4Interface
from typing import Literal, Optional, Union
from uuid import UUID

from more_itertools import first
from pydantic import Field, ValidationInfo, field_validator, AliasChoices

from pyfortinet.fmg_api import FMGObject

ADDRESS_GROUP_TYPE = Literal["default", "array", "folder"]
ADDRESS_GROUP_CATEGORY = Literal["default", "ztna-ems-tag", "ztna-geo-tag"]
ALLOW_ROUTING = Literal["disable", "enable"]
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


class Address(FMGObject):
    """Address class for high-level operations

    Attributes:
        name (str): object name
        associated_interface (str|list[str]): object assigned to interface/zone name
        subnet (str|list[str]): subnet in x.x.x.x/x or [x.x.x.x, y.y.y.y] format
    """

    _url: str = "/pm/config/{scope}/obj/firewall/address"
    name: str = Field(..., max_length=128)
    allow_routing: Optional[ALLOW_ROUTING] = Field(
        None, validation_alias=AliasChoices("allow-routing", "allow_routing"), serialization_alias="allow-routing"
    )
    associated_interface: Optional[Union[str, list[str]]] = Field(
        None,
        validation_alias=AliasChoices("associated-interface", "associated_interface"),
        serialization_alias="associated-interface",
    )
    subnet: Optional[Union[str, list[str]]] = None
    type: Optional[ADDRESS_TYPE] = None
    url: Optional[str] = None
    uuid: Optional[str] = None

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
    def validate_allow_routing(cls, v: int) -> ALLOW_ROUTING:
        return ALLOW_ROUTING.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("type", mode="before")
    def validate_type(cls, v: int) -> ADDRESS_TYPE:
        return ADDRESS_TYPE.__dict__.get("__args__")[v] if isinstance(v, int) else v


class AddressMapping(Address):
    _url: str = "/pm/config/{scope}/obj/firewall/address/{address}/dynamic_mapping"
    global_object: int = Field(
        ..., validation_alias=AliasChoices("global-object", "global_object"), serialization_alias="global-object"
    )


class AddressGroup(FMGObject):
    _url: str = "/pm/config/{scope}/obj/firewall/addrgrp"
    name: str
    member: list[Address]
    exclude_member: list[Address] = Field(
        ..., validation_alias=AliasChoices("exclude-member", "exclude_member"), serialization_alias="exclude-member"
    )
    comment: str = ""
    category: ADDRESS_GROUP_CATEGORY = "default"
    type: ADDRESS_GROUP_TYPE = "default"
    uuid: Optional[UUID]
    dynamic_mapping: list["AddressGroupMapping"]


class AddressGroupMapping(AddressGroup):
    _url: str = "/pm/config/{scope}/obj/firewall/addrgrp/{addrgrp}/dynamic_mapping"
    global_object: int = Field(
        ..., validation_alias=AliasChoices("global-object", "global_object"), serialization_alias="global-object"
    )

    @field_validator("_url", check_fields=False)
    def construct_url(cls, v: str, info: ValidationInfo):
        """rewrite URL with actual address group name"""
        url = v.replace("{addrgrp}", info.data["name"])
        return super().construct_url(url, info)
