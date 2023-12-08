"""Firewall object types"""
from ipaddress import IPv4Interface
from typing import Literal, Optional, Union
from uuid import UUID

from more_itertools import first
from pydantic import Field, ValidationInfo, field_validator

from pyfortinet.fmg_api import FMGObject

AddressGroupType = Literal["default", "array", "folder"]
AddressGroupCategory = Literal["default", "ztna-ems-tag", "ztna-geo-tag"]


class Address(FMGObject):
    """Address class for high-level operations

    Attributes:
        name (str): object name
        associated_interface (str|list[str]): object assigned to interface/zone name
        subnet (str|list[str]): subnet in x.x.x.x/x or [x.x.x.x, y.y.y.y] format
    """

    _url: str = "/pm/config/{scope}/obj/firewall/address"
    name: str
    associated_interface: Union[str, list[str]] = Field(None, serialization_alias="associated-interface")
    subnet: Union[str, list[str]] = None

    @field_validator("subnet")
    def standardize_subnet(cls, v):
        """validator: x.x.x.x/y.y.y.y -> x.x.x.x/y"""
        if isinstance(v, list):
            return IPv4Interface("/".join(v)).compressed
        else:
            return v

    @field_validator("associated_interface")
    def standardize_assoc_iface(cls, v):
        """validator: FMG sends a list with a single element, replace with single element"""
        if isinstance(v, list):
            return first(v, None)
        else:
            return v


class AddressMapping(Address):
    _url: str = "/pm/config/{scope}/obj/firewall/address/{address}/dynamic_mapping"
    global_object: int = Field(..., serialization_alias="global-object")


class AddressGroup(FMGObject):
    _url: str = "/pm/config/{scope}/obj/firewall/addrgrp"
    name: str
    member: list[Address]
    exclude_member: list[Address] = Field(..., serialization_alias="exclude-member")
    comment: str = ""
    category: AddressGroupCategory = "default"
    type: AddressGroupType = "default"
    uuid: Optional[UUID]
    dynamic_mapping: list["AddressGroupMapping"]


class AddressGroupMapping(AddressGroup):
    _url: str = "/pm/config/{scope}/obj/firewall/addrgrp/{addrgrp}/dynamic_mapping"
    global_object: int = Field(..., serialization_alias="global-object")

    @classmethod
    @field_validator("_url")
    def construct_url(cls, v: str, info: ValidationInfo):
        """rewrite URL with actual address group name"""
        url = v.replace("{addrgrp}", info.data["name"])
        return super().construct_url(url, info)
