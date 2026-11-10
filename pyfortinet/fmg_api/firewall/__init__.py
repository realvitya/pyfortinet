"""Public firewall classes."""

from pyfortinet.fmg_api.common import Scope

from .address import Address, AddressGroup, AddressTagging
from .internet_service import InternetService
from .ip_pool import IPPool, IPPoolDynamicMapping
from .ip_pool_group import IPPoolGroup
from .profile_group import ProfileGroup
from .proxy_address import ProxyAddress, ProxyAddressHeaderGroup, ProxyAddressTagging
from .proxy_address_group import ProxyAddressGroup, ProxyAddressGroupTagging
from .service import PortRange, ServiceCategory, ServiceCustom, ServiceGroup
from .vip import VIP, VIPDynamicMapping

__all__ = [
    "Address",
    "AddressGroup",
    "AddressTagging",
    "IPPool",
    "IPPoolDynamicMapping",
    "IPPoolGroup",
    "InternetService",
    "PortRange",
    "ProfileGroup",
    "ProxyAddress",
    "ProxyAddressGroup",
    "ProxyAddressGroupTagging",
    "ProxyAddressHeaderGroup",
    "ProxyAddressTagging",
    "Scope",
    "ServiceCategory",
    "ServiceCustom",
    "ServiceGroup",
    "VIP",
    "VIPDynamicMapping",
]
