"""Security console API"""
from typing import Optional, Literal, List

from pyfortinet.fmg_api import FMGExecObject, FMGObject
from pyfortinet.fmg_api.common import Scope

INSTALL_DEVICE_FLAGS = Literal["none", "preview", "auto_lock_ws"]


class InstallDeviceTask(FMGExecObject):
    """Install device settings

    Attributes:
        adom (str): ADOM to use
        dev_rev_comments (str): Device revision comments
        flags (List[INSTALL_DEVICE_FLAGS]): flags for the task
        scope (List[Scope]): scopes for the task (e.g. group name or device with vdom)
    """
    _url = "/securityconsole/install/device"
    adom: Optional[str] = None
    dev_rev_comments: Optional[str] = None
    flags: Optional[List[INSTALL_DEVICE_FLAGS]] = None
    scope: Optional[List[Scope]] = None
