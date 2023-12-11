"""Device Manager Command"""
from typing import Literal, Optional

from pydantic import Field

from pyfortinet.fmg_api import FMGExecObject, FMGObject
from pyfortinet.fmg_api.common import BaseDevice, Scope

FLAGS = Literal["none", "create_task", "nonblocking", "log_dev"]
DEVICE_ACTION = Literal["add_model", "promote_unreg"]


class Device(FMGObject, BaseDevice):
    """Device class to add"""

    # model devices only
    device_action: Optional[DEVICE_ACTION] = Field(None, serialization_alias="device action")
    device_blueprint: Optional[str] = Field(None, serialization_alias="device blueprint")
    mr: Optional[int] = None
    name: str  # mandatory
    platform_str: Optional[str] = None


class AddDevice(FMGExecObject):
    """Add device request"""

    # internal attributes
    _url = "/dvm/cmd/add/device"
    _params = {}
    # api attributes
    adom: str
    device: Device
    flags: list[FLAGS] = Field(default_factory=list)
    groups: list[Scope] = None
