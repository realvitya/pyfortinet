"""Device DB objects"""

from typing import Literal, Optional, List, Dict, Union

from pydantic import Field, field_validator, AliasChoices, BaseModel

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.exceptions import FMGException

ENABLE_DISABLE = Literal["disable", "enable"]


class PlatformMapping(FMGObject):
    _url = "/pm/config/{scope}/obj/dynamic/interface/{interface}/platform_mapping/{platform_mapping}"
    # URL fields
    interface: Optional[str] = None
    platform_mapping: Optional[str] = None
    # API fields
    egress_shaping_profile: Optional[List[str]] = Field(  # TODO: implement ShapingProfile
        None,
        validation_alias=AliasChoices("egress-shaping-profile", "egress_shaping_profile"),
        serialization_alias="egress-shaping-profile"
    )
    intf_zone: Optional[str] = Field(  # zone to map
        None,
        validation_alias=AliasChoices("intf-zone", "intf_zone"),
        serialization_alias="intf-zone"
    )
    intrazone_deny: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("intrazone-deny", "intrazone_deny"),
        serialization_alias="intrazone-deny"
    )
    name: Optional[str] = None  # Platform name
    oid: Optional[int] = None

    @property
    def get_url(self) -> str:
        """Derive URL for object based on initial URL fields

        Returns:
            URL string to call
        """
        url = super().get_url
        if self.interface is None:
            raise FMGException("interface field is required!")
        url = url.replace("{interface}", self.interface)
        if self.platform_mapping is None:
            url = url.replace("/{platform_mapping}", "")
        return url


class DynamicMapping(FMGObject):
    _url = "/pm/config/{scope}/obj/dynamic/interface/{interface}/dynamic_mapping/{dynamic_mapping_name}/{dynamic_mapping_vdom}"
    _master_keys = ["oid"]
    # URL fields
    interface: Optional[str] = None
    dynamic_mapping_name: Optional[str] = None
    dynamic_mapping_vdom: Optional[str] = None
    # API fields
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
    intrazone_deny: Optional[ENABLE_DISABLE] = Field(
        None,
        validation_alias=AliasChoices("intrazone-deny", "intrazone_deny"),
        serialization_alias="intrazone-deny"
    )
    local_intf: Optional[List[str]] = Field(
        None,
        validation_alias=AliasChoices("local-intf", "local_intf"),
        serialization_alias="local-intf"
    )
    oid: Optional[int] = None
    # Mapping fields
    mapping__scope: Optional[Union[Union[dict, Scope], List[Union[dict, Scope]]]] = Field(
        None, validation_alias=AliasChoices("_scope", "mapping__scope"), serialization_alias="_scope"
    )

    @property
    def get_url(self) -> str:
        """Derive URL for object based on initial URL fields

        Returns:
            URL string to call
        """
        url = super().get_url
        if self.interface is None:
            raise FMGException("interface field is required!")
        url = url.replace("{interface}", self.interface)
        if self.dynamic_mapping_name is None:
            url = url.replace("/{dynamic_mapping_name}/{dynamic_mapping_vdom}", "")
        elif self.dynamic_mapping_name and self.dynamic_mapping_vdom:
            url = url.replace("{dynamic_mapping_name}", self.dynamic_mapping_name)
            url = url.replace("{dynamic_mapping_vdom}", self.dynamic_mapping_vdom)
        else:
            raise FMGException("dynamic_mapping_name and dynamic_mapping_vdom both are required!")
        return url

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
    _master_keys = ["name"]
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
    dynamic_mapping: Optional[Union[List[DynamicMapping], DynamicMapping]] = None
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
    oid: Optional[int] = None
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
