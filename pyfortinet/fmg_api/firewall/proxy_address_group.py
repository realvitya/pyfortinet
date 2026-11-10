"""ProxyAddressGroup schema for FMG 7.6.7, FortiOS 7.4 ADOM objects.

Static declarations; no private schema file is needed at runtime.
"""

from typing import Literal, Optional

from pydantic import AliasChoices, BaseModel, Field, field_validator

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.firewall._values import as_list, reference_names, uuid_string


class ProxyAddressGroupTagging(BaseModel):
    """Fields for `pm.config.firewall.proxy-addrgrp.tagging`; omitted values are not written."""

    category: Optional[list[str]] = Field(None, description=("Tag category."))
    name: Optional[str] = Field(None, description=("Tagging entry name."))
    tags: Optional[list[str]] = Field(None, description=("Tags."))

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator("category", mode="before")
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)


class ProxyAddressGroup(FMGObject):
    """Fields for `pm.config.firewall.proxy-addrgrp`; omitted values are not written."""

    _url: str = "/pm/config/{scope}/obj/firewall/proxy-addrgrp/{proxy_addrgrp}"
    _master_keys = {"proxy_addrgrp": "name"}

    image_base64: Optional[str] = Field(
        None, validation_alias=AliasChoices("_image-base64", "image_base64"), serialization_alias="_image-base64"
    )
    color: Optional[int] = Field(
        None,
        description=(
            "Integer value to determine the color of the icon in the GUI (1 - 32, default = 0, which sets value to 1)."
        ),
    )
    comment: Optional[str] = Field(None, description=("Optional comments."))
    member: Optional[list[str]] = Field(None, description=("Members of address group."))
    name: Optional[str] = Field(None, description=("Address group name."))
    tagging: Optional[list[ProxyAddressGroupTagging]] = Field(None)
    type: Optional[Literal["src", "dst"]] = Field(None, description=("Source or destination address group type."))
    uuid: Optional[str] = Field(
        None, description=("Universally Unique Identifier (UUID; automatically assigned but can be manually reset).")
    )

    @field_validator("tagging", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator("member", mode="before")
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)

    @field_validator("uuid")
    @classmethod
    def normalize_uuid(cls, value: Optional[str]) -> Optional[str]:
        return uuid_string(value)
