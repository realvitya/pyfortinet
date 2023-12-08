"""Device DB objects"""
from typing import Literal, Optional

from pydantic import Field

from pyfortinet.fmg_api import FMGObject

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
MGMT_MODE = Literal["unreg", "fmg", "faz", "fmgfaz"]
OS_TYPE = Literal[
    "unknown",
    "fos",
    "fsw",
    "foc",
    "fml",
    "faz",
    "fwb",
    "fch",
    "fct",
    "log",
    "fmg",
    "fsa",
    "fdd",
    "fac",
    "fpx",
    "fna",
    "ffw",
    "fsr",
    "fad",
    "fdc",
    "fap",
    "fxt",
    "fts",
    "fai",
    "fwc",
    "fis",
    "fed",
]
OS_VER = Literal["unknown", "0.0", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"]
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


class Device(FMGObject):
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
    _url = ""
    # api attributes
    name: Optional[str]
    adm_usr: Optional[str]
    adm_pass: Optional[list[str]]
    app_ver: Optional[str]
    av_ver: Optional[str]
    checksum: Optional[str]
    conf_status: Optional[CONF_STATUS]
    conn_mode: Optional[CONN_MODE]
    ha_group_id: Optional[int]
    ha_group_name: Optional[str]
    hostname: Optional[str]
    ip: Optional[str]
    meta_fields: Optional[dict[str, str]] = Field(None, serialization_alias="meta fields")
    mgmt_if: Optional[str]
    mgmt_mode: Optional[MGMT_MODE]
    mgmt_uuid: Optional[str]
    mgt_vdom: Optional[str]
    os_type: Optional[OS_TYPE]
    os_ver: Optional[OS_VER]
    patch: Optional[int]
    psk: Optional[str]
    sn: Optional[str] = Field(None, description="Serial number")
    vdom: Optional[list[VDOM]]
    version: Optional[int]
