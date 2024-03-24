"""Security console API"""
from typing import Optional, Literal, List

from pyfortinet.fmg_api import FMGExecObject, FMGObject
from pyfortinet.fmg_api.common import Scope

INSTALL_DEVICE_FLAGS = Literal["none", "preview", "auto_lock_ws"]


class InstallDeviceTask(FMGExecObject):
    _url = "/securityconsole/install/device"
    adom: Optional[str] = None
    dev_rev_comments: Optional[str] = None
    flags: Optional[List[INSTALL_DEVICE_FLAGS]] = None
    scope: Optional[List[Scope]] = None
