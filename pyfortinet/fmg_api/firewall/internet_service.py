"""InternetService schema for FMG 7.6.7, FortiOS 7.4 ADOM objects.

Static declarations; no private schema file is needed at runtime.
"""

from typing import Literal, Optional

from pydantic import AliasChoices, Field

from pyfortinet.exceptions import FMGWrongRequestException
from pyfortinet.fmg_api import FMGObject


class InternetService(FMGObject):
    """Fields for `pm.config.firewall.internet-service`; omitted values are not written."""

    _url: str = "/pm/config/{scope}/obj/firewall/internet-service"
    _master_keys = {"id": "id"}

    database: Optional[Literal["isdb", "irdb"]] = Field(None)
    direction: Optional[Literal["src", "dst", "both"]] = Field(None)
    extra_ip_range_number: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("extra-ip-range-number", "extra_ip_range_number"),
        serialization_alias="extra-ip-range-number",
    )
    extra_ip6_range_number: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("extra-ip6-range-number", "extra_ip6_range_number"),
        serialization_alias="extra-ip6-range-number",
    )
    icon_id: Optional[int] = Field(
        None, validation_alias=AliasChoices("icon-id", "icon_id"), serialization_alias="icon-id"
    )
    id: Optional[int] = Field(None)
    ip_number: Optional[int] = Field(
        None, validation_alias=AliasChoices("ip-number", "ip_number"), serialization_alias="ip-number"
    )
    ip_range_number: Optional[int] = Field(
        None, validation_alias=AliasChoices("ip-range-number", "ip_range_number"), serialization_alias="ip-range-number"
    )
    ip6_range_number: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ip6-range-number", "ip6_range_number"),
        serialization_alias="ip6-range-number",
    )
    name: Optional[str] = Field(None)
    obsolete: Optional[int] = Field(None)
    singularity: Optional[int] = Field(None)

    def get_url(self, method: str = "get") -> str:
        if method not in ("get", "set", "update"):
            raise FMGWrongRequestException("InternetService supports only GET, SET, and UPDATE")
        return super().get_url(method)
