"""Fortinet Policy object"""
from ipaddress import IPv4Network
from typing import Literal, List, Union

from pydantic import BaseModel, Field

Action = Literal["deny", "accept", "ipsec", "ssl-vpn", "redirect", "isolate"]


class Policy(BaseModel):
    name: str
    action: Action = "deny"
    comments: str = ""
    dstaddr: List[Union[IPv4Network, AddressGroup]]
