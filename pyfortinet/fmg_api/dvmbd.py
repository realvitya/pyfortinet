"""Device DB objects"""
from typing import Literal, Optional

from pydantic import Field

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import BaseDevice

CONF_STATUS = Literal["unknown", "insync", "outofsync"]
CONN_MODE = Literal["active", "passive"]
CONN_STATUS = Literal["UNKNOWN", "up", "down"]
DB_STATUS = Literal["unknown", "nomod", "mod"]
DEV_STATUS = Literal[
    "none",
    "unknown",
    "checkedin",
    "inprogress",
    "installed",
    "aborted",
    "sched",
    "retry",
    "canceled",
    "pending",
    "retrieved",
    "changed_conf",
    "sync_fail",
    "timeout",
    "rev_revert",
    "auto_updated",
]
OP_MODE = Literal["nat", "transparent"]
VDOM_TYPE = Literal["traffic", "admin"]


class VDOM(FMGObject):
    """Device Virtual Domain"""

    # internal attributes
    _url = "/dvmdb{adom}/device/{device}/vdom"
    scope: str = Field("", exclude=True, description="ADOM to use (optional)")
    device: str = Field(..., exclude=True, description="Assigned device")
    # API attributes
    name: Optional[str]
    comments: Optional[str]
    meta_fields: Optional[dict[str, str]] = Field(None, serialization_alias="meta fields")
    opmode: Optional[OP_MODE]
    status: Optional[str]
    vdom_type: Optional[VDOM_TYPE]

    @property
    def url(self) -> str:
        """API URL where {scope} is replaced on the fly based on the FMG selected scope (adom or global)"""
        scope = f"adom/{self.adom}" if self.adom else ""
        url = self._url.replace("{adom}", scope).replace("{device}", self.device)
        return url


class Device(FMGObject, BaseDevice):
    """Device

    Attributes:
        name (str): object name
        adm_usr (str): admin user
        adm_pass (list[str]): admin password
        app_ver (str): App DB version
        av_ver (str): Anti-Virus DB version
        checksum (str): Configuration checksum
        conf_status (CONF_STATUS): Configuration status
    """

    # internal attributes
    _url = "/dvmdb{adom}/device"
    # api attributes
    app_ver: Optional[str]
    av_ver: Optional[str]
    checksum: Optional[str]
    conf_status: Optional[CONF_STATUS]
    conn_mode: Optional[CONN_MODE]
    conn_status: Optional[CONN_STATUS]
    ha_group_id: Optional[int]
    ha_group_name: Optional[str]
    hostname: Optional[str]
    mgmt_if: Optional[str]
    mgmt_uuid: Optional[str]
    mgt_vdom: Optional[str]
    psk: Optional[str]
    vdom: Optional[list[VDOM]]
    version: Optional[int]

    @property
    def url(self) -> str:
        """Device API URL assembly"""
        scope = "" if self.scope == "global" else f"/adom/{self.scope}"
        url = self._url.replace("{adom}", scope)
        return url
