"""ProxyAddress schema for FMG 7.6.7, FortiOS 7.4 ADOM objects.

Static declarations; no private schema file is needed at runtime.
"""

from typing import Literal, Optional

from pydantic import AliasChoices, BaseModel, Field, field_validator

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api._firewall_values import as_list, reference_names, uuid_string


class ProxyAddressHeaderGroup(BaseModel):
    """Fields for `pm.config.firewall.proxy-address.header-group`; omitted values are not written."""

    case_sensitivity: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("case-sensitivity", "case_sensitivity"),
        serialization_alias="case-sensitivity",
        description=("Case sensitivity in pattern."),
    )
    header: Optional[str] = Field(None, description=("HTTP header regular expression."))
    header_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("header-name", "header_name"),
        serialization_alias="header-name",
        description=("HTTP header."),
    )
    id: Optional[int] = Field(None, description=("ID."))

    @field_validator("case_sensitivity", mode="before")
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value


class ProxyAddressTagging(BaseModel):
    """Fields for `pm.config.firewall.proxy-address.tagging`; omitted values are not written."""

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


class ProxyAddress(FMGObject):
    """Fields for `pm.config.firewall.proxy-address`; omitted values are not written."""

    _url: str = "/pm/config/{scope}/obj/firewall/proxy-address/{proxy_address}"
    _master_keys = {"proxy_address": "name"}

    image_base64: Optional[str] = Field(
        None, validation_alias=AliasChoices("_image-base64", "image_base64"), serialization_alias="_image-base64"
    )
    application: Optional[list[str]] = Field(None, description=("SaaS application."))
    case_sensitivity: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("case-sensitivity", "case_sensitivity"),
        serialization_alias="case-sensitivity",
        description=("Enable to make the pattern case sensitive."),
    )
    category: Optional[list[str]] = Field(None, description=("FortiGuard category ID."))
    color: Optional[int] = Field(
        None,
        description=(
            "Integer value to determine the color of the icon in the GUI (1 - 32, default = 0, which sets value to 1)."
        ),
    )
    comment: Optional[str] = Field(None, description=("Optional comments."))
    header: Optional[str] = Field(None, description=("HTTP header name as a regular expression."))
    header_group: Optional[list[ProxyAddressHeaderGroup]] = Field(
        None, validation_alias=AliasChoices("header-group", "header_group"), serialization_alias="header-group"
    )
    header_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("header-name", "header_name"),
        serialization_alias="header-name",
        description=("Name of HTTP header."),
    )
    host: Optional[list[str]] = Field(None, description=("Address object for the host."))
    host_regex: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("host-regex", "host_regex"),
        serialization_alias="host-regex",
        description=("Host name as a regular expression."),
    )
    method: Optional[list[Literal["delete", "get", "head", "options", "post", "put", "trace", "connect"]]] = Field(
        None, description=("HTTP request methods to be used.")
    )
    name: Optional[str] = Field(None, description=("Address name."))
    path: Optional[str] = Field(None, description=("URL path as a regular expression."))
    query: Optional[str] = Field(None, description=("Match the query part of the URL as a regular expression."))
    referrer: Optional[Literal["disable", "enable"]] = Field(
        None, description=("Enable/disable use of referrer field in the HTTP header to match the address.")
    )
    tagging: Optional[list[ProxyAddressTagging]] = Field(None)
    type: Optional[
        Literal["host-regex", "url", "category", "method", "ua", "header", "src-advanced", "dst-advanced", "saas"]
    ] = Field(None, description=("Proxy address type."))
    ua: Optional[list[Literal["chrome", "ms", "firefox", "safari", "other", "ie", "edge"]]] = Field(
        None, description=("Names of browsers to be used as user agent.")
    )
    ua_max_ver: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ua-max-ver", "ua_max_ver"),
        serialization_alias="ua-max-ver",
        description=(
            "Maximum version of the user agent specified in dotted notation. For example, use 120 with "
            'the ua field set to "chrome" to require Google Chrome\'s maximum version must be 120.'
        ),
    )
    ua_min_ver: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ua-min-ver", "ua_min_ver"),
        serialization_alias="ua-min-ver",
        description=(
            "Minimum version of the user agent specified in dotted notation. For example, use 90.0.1 "
            'with the ua field set to "chrome" to require Google Chrome\'s minimum version must be '
            "90.0.1."
        ),
    )
    uuid: Optional[str] = Field(
        None, description=("Universally Unique Identifier (UUID; automatically assigned but can be manually reset).")
    )

    @field_validator("application", "header_group", "method", "tagging", "ua", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator("category", "host", mode="before")
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)

    @field_validator("case_sensitivity", "referrer", mode="before")
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value

    @field_validator("uuid")
    @classmethod
    def normalize_uuid(cls, value: Optional[str]) -> Optional[str]:
        return uuid_string(value)
