"""Device Manager Command"""
from typing import Literal, Optional, Union, List, Dict

from pydantic import Field, model_validator, IPvAnyAddress, field_validator, BaseModel

from pyfortinet.fmg_api import FMGExecObject, FMGObject
from pyfortinet.fmg_api.common import Scope

FLAGS = Literal["none", "create_task", "nonblocking", "log_dev"]
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


class BaseDevice(BaseModel):
    # api attributes
    name: Optional[str] = Field(None, pattern=r"[\w-]{1,36}")
    adm_usr: Optional[str] = Field(None, max_length=36)
    adm_pass: Union[None, str, list[str]] = Field(None, max_length=128)
    desc: Optional[str] = None
    ip: Optional[str] = None
    meta_fields: Optional[dict[str, str]] = Field(None, alias="meta fields", serialization_alias="meta fields")
    mgmt_mode: Optional[MGMT_MODE] = None
    os_type: Optional[OS_TYPE] = None
    os_ver: Optional[OS_VER] = Field(None, description="Major release no")
    mr: Optional[int] = Field(None, description="Minor release no")
    patch: Optional[int] = Field(None, description="Patch release no")
    sn: Optional[str] = Field(None, description="Serial number")
    device_action: Optional[DEVICE_ACTION] = Field(None, alias="device action", serialization_alias="device action")
    device_blueprint: Optional[str] = Field(None, alias="device blueprint", serialization_alias="device blueprint")
    # extra attributes
    assignment_info: Optional[List[Dict[str, str]]] = Field(None, alias="assignment info", serialization_alias="assignment info", exclude=True)

    @field_validator("ip")
    def validate_ip(cls, v):
        """validate input but still represent the string"""
        IPvAnyAddress(v)
        return v

    @field_validator("mgmt_mode", mode="before")
    def validate_mgmt_mode(cls, v):
        """ensure using text variant"""
        if isinstance(v, str):
            return v
        return MGMT_MODE.__dict__.get("__args__")[v]

    @field_validator("os_type", mode="before")
    def validate_os_type(cls, v):
        """ensure using text variant"""
        if isinstance(v, str):
            return v
        return OS_TYPE.__dict__.get("__args__")[v]

    @field_validator("os_ver", mode="before")
    def validate_os_ver(cls, v):
        """ensure using text variant"""
        if isinstance(v, str):
            return v
        elif isinstance(v, int):
            return OS_VER.__dict__.get("__args__")[v]
        raise ValueError(f"Wrong OS version type: {type(v)}")


class Device(FMGObject, BaseDevice):
    """Device class to add"""

    name: str = Field(..., pattern=r"[\w-]{1,36}")
    device_action: Union[Literal[""], DEVICE_ACTION] = Field("", description="Leave empty for real device!", alias="device action",
                                                             serialization_alias="device action")
    adm_usr: str = Field("admin", pattern=r"[\w-]{1,36}")
    adm_pass: str = Field(..., max_length=128)
    ip: str


class ModelDevice(FMGObject, BaseDevice):
    """Model device fields"""

    device_action: DEVICE_ACTION = Field("add_model", alias="device action", serialization_alias="device action")
    # device_blueprint: Optional[str] = Field(None, serialization_alias="device blueprint")
    name: str = Field(..., pattern=r"[\w-]{1,36}")
    platform_str: Optional[str] = None
    # make os_ver and mr mandatory
    os_ver: OS_VER
    mr: int = Field(description="Minor release")
    # set default
    os_type: OS_TYPE = "fos"
    mgmt_mode: MGMT_MODE = "fmg"


class DeviceTask(FMGExecObject):
    """Add/Del device request

    Attributes:
        action (Literal["add","del"]): Add or Del device
        adom: ADOM to use
        device: Device to add/del
        flags (List[FLAGS]): Job flags
        groups (List[Scope]): device groups
    """

    # internal attributes
    _url = "/dvm/cmd/{action}/device"
    _params = {}
    action: Literal["add", "del"] = Field("add", exclude=True, validate_default=True)
    # api attributes
    adom: str
    device: Union[str, Device, ModelDevice]
    flags: list[FLAGS] = Field(["create_task", "non-blocking"])
    groups: list[Scope] = None

    @model_validator(mode="after")
    def validate_devicejob(self) -> "DeviceTask":
        """Validate device job"""
        self._url = self._url.replace("{action}", self.action)
        if self.action == "del":
            self.device = self.device.name  # deleting a device requires device id or name
        return self
