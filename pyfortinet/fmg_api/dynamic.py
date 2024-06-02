"""Device DB objects"""

from typing import Literal, Optional, List, Dict, Union

from pydantic import Field, field_validator, AliasChoices, BaseModel

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.system import DeviceInterface

ENABLE_DISABLE = Literal["disable", "enable"]


class PlatformMapping(BaseModel):
    egress_shaping_profile: Optional[List[str]] = Field(  # TODO: implement ShapingProfile
        None,
        validation_alias=AliasChoices("egress-shaping-profile", "egress_shaping_profile"),
        serialization_alias="egress-shaping-profile"
    )
    intf_zone: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("intf-zone", "intf_zone"),
        serialization_alias="intf-zone"
    )
    intrazone_deny: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("intrazone-deny", "intrazone_deny"),
        serialization_alias="intrazone-deny"
    )
    name: Optional[str] = None


class NormalizedInterface(FMGObject):
    """Interface object

    Attributes:
        interface:
        color:
        default_mapping:
        defmap_intf:
        defmap_intrazone_deny:
        defmap_zonemember:
        description:
        dynamic_mapping:
        egress_shaping_profile:
        ingress_shaping_profile:
        name:
        platform_mapping:
        single_intf:
        wildcard:
        wildcard_intf_zone_only:
        mapping__scope:
        local_intf:
    """
    _url = "/pm/config/{scope}/obj/dynamic/interface/{interface}"
    # URL fields
    interface: Optional[str] = Field(None, exclude=True)
    # API fields
    color: Optional[int] = None
    default_mapping: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("default-mapping", "default_mapping"),
        serialization_alias="default-mapping"
    )
    defmap_intf: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("defmap-intf", "defmap_intf"),
        serialization_alias="defmap-intf"
    )
    defmap_intrazone_deny: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("defmap-intrazone-deny", "defmap_intrazone_deny"),
        serialization_alias="defmap-intrazone-deny"
    )
    defmap_zonemember: Optional[List[str]] = Field(
        None,
        validation_alias=AliasChoices("defmap-zonemember", "defmap_zonemember"),
        serialization_alias="defmap-zonemember"
    )
    description: Optional[str] = None
    dynamic_mapping: Optional[Union[List[DeviceInterface], DeviceInterface]] = None
    egress_shaping_profile: Optional[List[str]] = Field(  # TODO: implement ShapingProfile
        None,
        validation_alias=AliasChoices("egress-shaping-profile", "egress_shaping_profile"),
        serialization_alias="egress-shaping-profile"
    )
    ingress_shaping_profile: Optional[List[str]] = Field(  # TODO: implement ShapingProfile
        None,
        validation_alias=AliasChoices("ingress-shaping-profile", "ingress_shaping_profile"),
        serialization_alias="ingress-shaping-profile"
    )
    name: Optional[str] = None
    platform_mapping: Optional[List[Union[str, PlatformMapping]]] = None
    single_intf: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("single-intf", "single_intf"),
        serialization_alias="single-intf"
    )
    wildcard: Optional[ENABLE_DISABLE] = None
    wildcard_intf_zone_only: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("only-wildcard-intf-zone", "wildcard_intf_zone_only"),
        serialization_alias="wildcard-intf-zone-only"
    )

    # Mapping fields
    mapping__scope: Optional[Union[Union[dict, Scope], List[Union[dict, Scope]]]] = Field(
        None, validation_alias=AliasChoices("_scope", "mapping__scope"), serialization_alias="_scope"
    )
    local_intf: Optional[List[str]] = Field(
        None,
        validation_alias=AliasChoices("local-intf", "local_intf"),
        serialization_alias="local-intf"
    )

    @property
    def get_url(self) -> str:
        url = super().get_url
        if self.interface is None:
            url = url.replace("/{interface}", "")
        else:
            url = url.replace("{interface}", self.interface)
        return url
