"""Device DB objects"""

from typing import Literal, Optional, List, Dict, Union

from pydantic import Field, field_validator, AliasChoices, BaseModel, IPvAnyAddress

from pyfortinet.exceptions import FMGException
from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import Scope


ADOM_FLAGS = Literal[
    "migration",
    "db_export",
    "no_vpn_console",
    "backup",
    "other_devices",
    "is_autosync",
    "per_device_wtp",
    "policy_check_on_install",
    "install_on_policy_check_fail",
    "auto_push_cfg",
    "per_device_fsw",
]
ADOM_MODE = Literal["ems", "gms", "provider"]
ADOM_RESTRICTED_PRDS = Literal[
    "fos",
    "foc",
    "fml",
    "fch",
    "fwb",
    "log",
    "fct",
    "faz",
    "fsa",
    "fsw",
    "fmg",
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
    "fpa",
    "fabric",
]
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
DEVICE_ACTION = Literal["add_model", "promote_unreg"]


class VDOM(FMGObject):
    """Device Virtual Domain"""

    # internal attributes
    _url = "/dvmdb/{scope}/device/{device}/vdom"
    _master_keys = ["name"]
    # API attributes
    device: str = Field("", exclude=True, description="Assigned device")
    name: Optional[str] = None
    comments: Optional[str] = None
    meta_fields: Optional[dict[str, str]] = Field(
        None, validation_alias=AliasChoices("meta fields", "meta_fields"), serialization_alias="meta fields"
    )
    opmode: Optional[OP_MODE] = None
    status: Optional[str] = None
    vdom_type: Optional[VDOM_TYPE] = None
    # extra attributes
    assignment_info: Optional[List[Dict[str, str]]] = Field(
        None,
        validation_alias=AliasChoices("assignment info", "assignment_info"),
        serialization_alias="assignment info",
        exclude=True,
    )

    @field_validator("opmode", mode="before")
    def validate_opmode(cls, v) -> OP_MODE:
        return OP_MODE.__dict__.get("__args__")[v - 1] if isinstance(v, int) else v

    @field_validator("vdom_type", mode="before")
    def validate_vdom_type(cls, v) -> VDOM_TYPE:
        return VDOM_TYPE.__dict__.get("__args__")[v - 1] if isinstance(v, int) else v

    @property
    def get_url(self) -> str:
        url = super().get_url
        if self.device is None:
            raise FMGException("device field is required!")
        url = url.replace("{device}", self.device)
        return url


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
    def validate_conf_status(cls, v) -> CONF_STATUS:
        return CONF_STATUS.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("role", mode="before")
    def validate_role(cls, v) -> ROLE:
        return ROLE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("status", mode="before")
    def validate_status(cls, v) -> CONN_STATUS:
        return CONN_STATUS.__dict__.get("__args__")[v] if isinstance(v, int) else v


class Device(FMGObject):
    """ADOM level Device object

    Attributes:
        device (str): device name to target by API call
        name (str): object name
        adm_usr (str): admin user
        adm_pass (list[str]): admin password
        app_ver (str): App DB version
        av_ver (str): Anti-Virus DB version
        checksum (str): Configuration checksum
        conf_status (CONF_STATUS): Configuration status
        desc (str): Device description
        ha_group_id (int): HA group ID
        ha_group_name (str): HA group Name
        hostname (str): hostname
        ip (str): Device IP address
        meta_fields (dict): Meta fields data
        mgmt_if (str): management interface name
        mgmt_mode (MGMT_MODE): Management mode of the device
        mgmt_uuid (str):
        mgt_vdom (str): management VDOM
        mr (int): OS minor version
        os_type (OS_TYPE): OS type of the device
        os_ver (OS_VER): OS major version
        patch (int): OS patch version
        psk (str): pre-shared secret
        sn (str): Serial number of the device
        version (int):
        platform_str (str): platform name (device model)
        vdom (list[VDOM]): VDOM list
        ha_slave: Optional[List[HASlave]]
    """

    # internal attributes
    _url = "/dvmdb/{scope}/device/{device}"
    # URL attributes
    device: Optional[str] = Field(None, exclude=True, description="Assigned device")
    # api attributes
    adm_usr: Optional[str] = Field(None, max_length=36)
    adm_pass: Optional[Union[str, list[str]]] = Field(None, max_length=128)
    app_ver: Optional[str] = Field(None, description="App DB version", exclude=True)
    assignment_info: Optional[List[Dict[str, str]]] = Field(
        None,
        validation_alias=AliasChoices("assignment info", "assignment_info"),
        serialization_alias="assignment info",
        exclude=True,
    )
    av_ver: Optional[str] = Field(None, description="Anti-Virus DB", exclude=True)
    checksum: Optional[str] = Field(None, exclude=True)
    conf_status: Optional[CONF_STATUS] = Field(None, exclude=True)
    conn_mode: Optional[CONN_MODE] = Field(None, exclude=True)
    conn_status: Optional[CONN_STATUS] = Field(None, exclude=True)
    desc: Optional[str] = None
    ha_group_id: Optional[int] = None
    ha_group_name: Optional[str] = None
    hostname: Optional[str] = None
    ip: Optional[str] = None
    meta_fields: Optional[dict[str, str]] = Field(
        None, validation_alias=AliasChoices("meta fields", "meta_fields"), serialization_alias="meta fields"
    )
    mgmt_if: Optional[str] = None
    mgmt_mode: Optional[MGMT_MODE] = None
    mgmt_uuid: Optional[str] = None
    mgt_vdom: Optional[str] = None
    mr: Optional[int] = Field(None, description="Minor release no")
    name: Optional[str] = Field(None, pattern=r"[\w-]{1,36}")  # master key, mandatory
    os_type: Optional[OS_TYPE] = None
    os_ver: Optional[OS_VER] = Field(None, description="Major release no")
    patch: Optional[int] = Field(None, description="Patch release no")
    psk: Optional[str] = None
    version: Optional[int] = None
    platform_str: Optional[str] = None
    sn: Optional[str] = Field(None, description="Serial number")
    # sub objects:
    vdom: Optional[list[VDOM]] = Field(None, exclude=True)
    ha_slave: Optional[List[HASlave]] = None

    @field_validator("ip")
    def validate_ip(cls, v):
        """validate input but still represent the string"""
        if v:
            assert IPvAnyAddress(v)
        return v

    @field_validator("mgmt_mode", mode="before")
    def validate_mgmt_mode(cls, v):
        """ensure using text variant"""
        return MGMT_MODE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("os_type", mode="before")
    def validate_os_type(cls, v):
        """ensure using text variant"""
        return OS_TYPE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("os_ver", mode="before")
    def validate_os_ver(cls, v):
        """ensure using text variant"""
        return OS_VER.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("conf_status", mode="before")
    def validate_conf_status(cls, v) -> CONF_STATUS:
        """ensure using text variant"""
        return CONF_STATUS.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("conn_mode", mode="before")
    def validate_conn_mode(cls, v) -> CONN_MODE:
        """ensure using text variant"""
        return CONN_MODE.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @field_validator("conn_status", mode="before")
    def validate_conn_type(cls, v) -> CONN_STATUS:
        """ensure using text variant"""
        return CONN_STATUS.__dict__.get("__args__")[v] if isinstance(v, int) else v

    @property
    def get_url(self) -> str:
        url = super().get_url
        if self.device is None:
            url = url.replace("/{device}", "")
        else:
            url = url.replace("{device}", self.device)
        return url

    def get_vdom_scope(self, vdom: str) -> Optional[Scope]:
        """Get Scope for a VDOM to be used by filters

        Returns:
            (Scope or None): The scope for the given VDOM
        """
        if vdom in (s_vdom.name for s_vdom in self.vdom):
            return Scope(name=self.name, vdom=vdom)
        return None


class ADOM(FMGObject):
    """ADOM object

    Attributes:
        create_time:
        desc:
        flags:
        log_db_retention_hours:
        log_disk_quota:
        log_disk_quota_alert_thres:
        log_disk_quota_split_ratio:
        log_file_retention_hours:
        meta_fields:
        mig_mr:
        mig_os_ver:
        mode:
        mr:
        name:
        os_ver:
        restricted_prds:
        state:
        uuid:
        workspace_mode:
    """

    _url = "/dvmdb/adom"
    _master_keys = ["name"]

    create_time: Optional[int] = None
    desc: Optional[str] = None
    flags: Optional[Union[ADOM_FLAGS, List[ADOM_FLAGS]]] = None
    log_db_retention_hours: Optional[int] = None
    log_disk_quota: Optional[int] = None
    log_disk_quota_alert_thres: Optional[int] = None
    log_disk_quota_split_ratio: Optional[int] = None
    log_file_retention_hours: Optional[int] = None
    meta_fields: Optional[dict[str, str]] = Field(
        None, validation_alias=AliasChoices("meta fields", "meta_fields"), serialization_alias="meta fields"
    )
    mig_mr: Optional[int] = None
    mig_os_ver: Optional[OS_VER] = None
    mode: Optional[ADOM_MODE] = None
    mr: Optional[int] = None
    name: Optional[str] = None
    os_ver: Optional[OS_VER] = None
    restricted_prds: Optional[ADOM_RESTRICTED_PRDS] = None
    state: Optional[int] = None
    uuid: Optional[str] = None
    workspace_mode: Optional[int] = None
