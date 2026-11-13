"""IPPoolGroup schema for FMG 7.6.7, FortiOS 7.4 ADOM objects.

Static declarations; no private schema file is needed at runtime.
"""

from typing import Optional

from pydantic import Field, field_validator

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.firewall._values import reference_names, uuid_string


class IPPoolGroup(FMGObject):
    """Fields for `pm.config.firewall.ippool_grp`; omitted values are not written."""

    _url: str = "/pm/config/{scope}/obj/firewall/ippool_grp/{ippool_grp}"
    _master_keys = {"ippool_grp": "name"}

    comments: Optional[str] = Field(None, description=("Comment."))
    member: Optional[list[str]] = Field(
        None, description=("Member IP pool of the group (They must have same attributes except public/client ranges).")
    )
    name: Optional[str] = Field(None, description=("IPPOOL group name."))
    uuid: Optional[str] = Field(
        None, description=("Universally Unique Identifier (UUID; automatically assigned but can be manually reset).")
    )

    @field_validator("member", mode="before")
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)

    @field_validator("uuid")
    @classmethod
    def normalize_uuid(cls, value: Optional[str]) -> Optional[str]:
        return uuid_string(value)
