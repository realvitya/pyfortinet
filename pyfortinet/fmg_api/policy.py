"""Fortinet Policy object"""

from typing import Literal, Union

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.firewall import Address, AddressGroup

Action = Literal["deny", "accept", "ipsec", "ssl-vpn", "redirect", "isolate"]


class Policy(FMGObject):
    _url = "/pm/config/adom/{adom}/pkg/{pkg}/firewall/policy"
    name: str
    action: Action = "deny"
    comments: str = None
    dstaddr: list[Union[Address, AddressGroup]]
