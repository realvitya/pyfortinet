"""Device DB objects"""

from typing import Literal, Optional, List, Dict

from pydantic import Field, field_validator, AliasChoices

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.dvmcmd import BaseDevice

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
    _url = "/dvmdb/{scope}/device/{device}/vdom"
    device: str = Field("", exclude=True, description="Assigned device (optional)")
    # API attributes
    name: Optional[str]
    comments: Optional[str]
    meta_fields: Optional[dict[str, str]] = Field(
        None, validation_alias=AliasChoices("meta fields", "meta_fields"), serialization_alias="meta fields"
    )
    opmode: Optional[OP_MODE]
    status: Optional[str]
    vdom_type: Optional[VDOM_TYPE]
    # extra attributes
    assignment_info: Optional[List[Dict[str, str]]] = Field(
        None,
        validation_alias=AliasChoices("assignment info", "assignment_info"),
        serialization_alias="assignment info",
        exclude=True,
    )

    @field_validator("opmode", mode="before")
    def validate_opmode(cls, v: int) -> OP_MODE:
        return OP_MODE.__dict__.get("__args__")[v-1] if isinstance(v, int) else v

    @field_validator("vdom_type", mode="before")
    def validate_vdom_type(cls, v: int) -> VDOM_TYPE:
        return VDOM_TYPE.__dict__.get("__args__")[v-1] if isinstance(v, int) else v


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
        return CONF_STATUS.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("role", mode="before")
    def validate_role(cls, v: int) -> ROLE:
        return ROLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("status", mode="before")
    def validate_status(cls, v: int) -> CONN_STATUS:
        return CONN_STATUS.__dict__.get("__args__")[v] if isinstance(v, int) else v


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
    _url = "/dvmdb/{scope}/device"
    # api attributes
    app_ver: Optional[str] = Field(None, description="App DB version", exclude=True)
    av_ver: Optional[str] = Field(None, description="Anti-Virus DB", exclude=True)
    checksum: Optional[str] = Field(None, exclude=True)
    conf_status: Optional[CONF_STATUS] = Field(None, exclude=True)
    conn_mode: Optional[CONN_MODE] = Field(None, exclude=True)
    conn_status: Optional[CONN_STATUS] = Field(None, exclude=True)
    ha_group_id: Optional[int] = None
    ha_group_name: Optional[str] = None
    hostname: Optional[str] = None
    mgmt_if: Optional[str] = None
    mgmt_uuid: Optional[str] = None
    mgt_vdom: Optional[str] = None
    psk: Optional[str] = None
    version: Optional[int] = None
    platform_str: Optional[str] = None
    # sub objects:
    vdom: Optional[list[VDOM]] = None
    ha_slave: Optional[List[HASlave]] = None

    @field_validator("conf_status", mode="before")
    def validate_conf_status(cls, v: int) -> CONF_STATUS:
        return CONF_STATUS.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("conn_mode", mode="before")
    def validate_conn_mode(cls, v: int) -> CONN_MODE:
        return CONN_MODE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("conn_status", mode="before")
    def validate_conn_type(cls, v: int) -> CONN_STATUS:
        return CONN_STATUS.__dict__.get("__args__")[v] if isinstance(v, int) else v
