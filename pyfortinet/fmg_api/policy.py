"""Fortinet Policy object"""

from typing import Literal, Union, Optional

from pydantic import BaseModel, AliasChoices, Field, field_validator

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.firewall import Address, AddressGroup

ACTION = Literal["deny", "accept", "ipsec", "ssl-vpn", "redirect", "isolate"]
ENABLE_DISABLE = Literal["disable", "enable"]
INSPECTION_MODE = Literal["proxy", "flow"]
NGFW_MODE = Literal["profile-based", "policy-based"]
POLICY_OFFLOAD_LEVEL = Literal["disable", "default", "dos-offload", "full-offload"]


class PackageSettings(BaseModel):
    """Package Settings class

    Attributes:

    """
    central_nat: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("central-nat", "central_nat"),
        serialization_alias="central-nat"
    )
    consolidated_firewall_mode: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("consolidated-firewall-mode", "consolidated_firewall_mode"),
        serialization_alias="consolidated-firewall-mode"
    )
    firewall_mode: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("firewall-mode", "firewall_mode"),
        serialization_alias="firewall-mode"
    )
    fwpolicy_implicit_log: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fwpolicy-implicit-log", "fwpolicy_implicit_log"),
        serialization_alias="fwpolicy-implicit-log"
    )
    fwpolicy6_implicit_log: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("fwpolicy6-implicit-log", "fwpolicy6_implicit_log"),
        serialization_alias="fwpolicy6-implicit-log"
    )
    inspection_mode: Optional[INSPECTION_MODE] = Field(
        None,
        validation_alias=AliasChoices("inspection-mode", "inspection_mode"),
        serialization_alias="inspection_mode"
    )
    ngfw_mode: Optional[NGFW_MODE] = Field(
        None,
        validation_alias=AliasChoices("ngfw-mode", "ngfw_mode"),
        serialization_alias="ngfw-mode"
    )
    policy_offload_level: Optional[POLICY_OFFLOAD_LEVEL] = Field(
        None,
        validation_alias=AliasChoices("policy-offload-level", "policy_offload_level"),
        serialization_alias="policy-offload-level"
    )
    ssl_ssh_profile: Optional[str] = None  # TODO: implement SSLSSHProfile

    @field_validator("central_nat", "consolidated_firewall_mode", "firewall_mode", "fwpolicy_implicit_log", "fwpolicy6_implicit_log", mode="before")
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


class PolicyPackage(FMGObject):
    """Policy Package class

    In the URL, {name} is optional and get_url function takes care of it.
    """
    _url = "/pm/pkg/{scope}"


class Policy(FMGObject):
    _url = "/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy"
    name: str
    action: ACTION = "deny"
    comments: str = None
    dstaddr: list[Union[Address, AddressGroup]]
