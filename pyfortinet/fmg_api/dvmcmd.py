"""Device Manager Command"""

from typing import Literal, Union, List, Optional

from pydantic import Field, model_validator

from pyfortinet.fmg_api import FMGExecObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.dvmdb import RealDevice, ModelDevice

FLAGS = Literal["none", "create_task", "nonblocking", "log_dev"]


class DeviceTask(FMGExecObject):
    """Add/Del device request

    Attributes:
        action (Literal["add","del"]): Add or Del device
        adom: ADOM to use
        device (Union[str, DeviceAction, ModelDevice]): Device to add/del
        flags (List[FLAGS]): Job flags
        groups (List[Scope]): device groups
    """

    # internal attributes
    _url = "/dvm/cmd/{action}/device"
    _params = {}
    action: Literal["add", "del"] = Field("add", exclude=True, validate_default=True)
    # api attributes
    adom: str
    device: Union[str, RealDevice, ModelDevice]
    flags: list[FLAGS] = ["create_task", "non-blocking"]
    groups: Optional[list[Scope]] = None

    @model_validator(mode="after")
    def validate_devicejob(self) -> "DeviceTask":
        """Validate device job"""
        self._url = self._url.replace("{action}", self.action)
        if self.action == "del":
            self.device = self.device.name  # deleting a device requires device id or name
        return self
