"""Device Manager Command"""
from typing import Literal, Optional, Union

from pydantic import Field, model_validator, IPvAnyAddress, field_validator

from pyfortinet.fmg_api import FMGExecObject, FMGObject
from pyfortinet.fmg_api.common import BaseDevice, Scope, OS_VER, OS_TYPE, MGMT_MODE, DEVICE_ACTION

FLAGS = Literal["none", "create_task", "nonblocking", "log_dev"]


class Device(FMGObject, BaseDevice):
    """Device class to add"""

    name: str = Field(..., pattern=r"[\w-]{1,36}")
    device_action: Union[Literal[""], DEVICE_ACTION] = Field("", description="Leave empty for real device!",
                                                             serialization_alias="device action")
    adm_usr: str = Field("admin", pattern=r"[\w-]{1,36}")
    adm_pass: str = Field(..., max_length=128)
    ip: str


class ModelDevice(FMGObject, BaseDevice):
    """Model device fields"""

    device_action: DEVICE_ACTION = Field("add_model", serialization_alias="device action")
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
