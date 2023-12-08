"""Device Manager Command"""
from typing import Literal

from pydantic import Field

from pyfortinet.fmg_api import FMGExecObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.dvmbd import Device

FLAGS = Literal["none", "create_task", "nonblocking", "log_dev"]


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
