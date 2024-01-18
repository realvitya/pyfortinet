"""Device Manager Command"""
from typing import Literal, Optional, Union

from pydantic import Field

from pyfortinet.fmg_api import FMGExecObject, FMGObject
from pyfortinet.fmg_api.common import BaseDevice, Scope, OS_VER, OS_TYPE, MGMT_MODE

FLAGS = Literal["none", "create_task", "nonblocking", "log_dev"]
DEVICE_ACTION = Literal["add_model", "promote_unreg"]


class Device(FMGObject, BaseDevice):
    """Device class to add"""

    # model devices only
    name: str  # mandatory


class ModelDevice(FMGObject, BaseDevice):
    """Model device fields"""
    device_action: DEVICE_ACTION = Field("add_model", serialization_alias="device action")
    device_blueprint: Optional[str] = Field(None, serialization_alias="device blueprint")
    name: str = Field(..., pattern=r"[\w-]{1,48}")
    platform_str: Optional[str] = None
    os_ver: OS_VER
    mr: int = Field(description="Minor release")
    os_type: OS_TYPE = "fos"
    mgmt_mode: MGMT_MODE = "fmg"
    adm_usr: str = "admin"


class AddDevice(FMGExecObject):
    """Add device request"""

    # internal attributes
    _url = "/dvm/cmd/add/device"
    _params = {}
    # api attributes
    adom: str
    device: Union[Device, ModelDevice]
    flags: list[FLAGS] = Field(["create_task"])
    groups: list[Scope] = None
