"""Device DB objects"""
from typing import Literal, Optional, List

from pydantic import Field, field_validator

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
    # scope: str = Field("", exclude=True, description="ADOM to use (optional)")
    device: str = Field("", exclude=True, description="Assigned device (optional)")
    # API attributes
    name: Optional[str]
    comments: Optional[str]
    meta_fields: Optional[dict[str, str]] = Field(None, serialization_alias="meta fields")
    opmode: Optional[OP_MODE]
    status: Optional[str]
    vdom_type: Optional[VDOM_TYPE]

    # @property
    # def get_url(self) -> str:
    #     """API URL where {scope} is replaced on the fly based on the FMG selected scope (adom or global)"""
    #     scope = f"adom/{self.adom}" if self.adom else ""
    #     url = self._url.replace("{adom}", scope).replace("{device}", self.device)
    #     return url

    @field_validator("opmode", mode="before")
    def validate_opmode(cls, v: int) -> OP_MODE:
        return OP_MODE.__dict__.get("__args__")[v]

    @field_validator("vdom_type", mode="before")
    def validate_vdom_type(cls, v: int) -> VDOM_TYPE:
        return VDOM_TYPE.__dict__.get("__args__")[v]


ROLE = Literal["slave", "master"]


class HASlave(FMGObject):
    """HA Slave object to inspect HA members

    Attributes:
        conf_status (CONF_STATUS): member HA config sync status (with other members)
        #did (str): device ID (cluster name)
        #flags: undocumented
        idx (int): device number in cluster (0,1)
        name (str): member device name
        #oid (int): undocumented
        prio (int): HA priority
        role (ROLE): member role
        sn (str): serial number
        status (CONN_STATUS): status of HA member
    """

    conf_status: CONF_STATUS
    idx: int
    name: str
    prio: int
    role: ROLE
    sn: str
    status: CONN_STATUS

    @field_validator("conf_status", mode="before")
    def validate_conf_status(cls, v: int) -> CONF_STATUS:
        return CONF_STATUS.__dict__.get("__args__")[v]

    @field_validator("role", mode="before")
    def validate_role(cls, v: int) -> ROLE:
        return ROLE.__dict__.get("__args__")[v]

    @field_validator("status", mode="before")
    def validate_status(cls, v: int) -> CONN_STATUS:
        return CONN_STATUS.__dict__.get("__args__")[v]


class Device(FMGObject, BaseDevice):
    """ADOM level read-only Device object

    Attributes:
        name (str): object name
        adm_usr (str): admin user
        adm_pass (list[str]): admin password
        app_ver (str): App DB version
        av_ver (str): Anti-Virus DB version
        checksum (str): Configuration checksum
        conf_status (CONF_STATUS): Configuration status
        ha_group_id (int): HA group ID
        ha_group_name (str): HA group Name
        hostname (str): hostname
        mgmt_if (str): management interface name
        mgmt_uuid (str):
        mgt_vdom (str): management VDOM
        psk (str): pre-shared secret
        version (int):
        platform_str (str): platform name (device model)
        vdom (list[VDOM]): VDOM list
        ha_slave: Optional[List[HASlave]]
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
    version: Optional[int]
    platform_str: Optional[str]
    # sub objects:
    vdom: Optional[list[VDOM]]
    ha_slave: Optional[List[HASlave]]

    # @property
    # def get_url(self) -> str:
    #     """Device API URL assembly"""
    #     scope = "" if self.scope == "global" else f"/adom/{self.scope}"
    #     url = self._url.replace("{adom}", scope)
    #     return url

    @field_validator("conf_status", mode="before")
    def validate_conf_status(cls, v: int) -> CONF_STATUS:
        return CONF_STATUS.__dict__.get("__args__")[v]

    @field_validator("conn_mode", mode="before")
    def validate_conn_mode(cls, v: int) -> CONN_MODE:
        return CONN_MODE.__dict__.get("__args__")[v]

    @field_validator("conn_status", mode="before")
    def validate_conn_type(cls, v: int) -> CONN_STATUS:
        return CONN_STATUS.__dict__.get("__args__")[v]
