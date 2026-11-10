"""Public firewall objects; existing imports remain available from this package."""

from pyfortinet.fmg_api.common import Scope

from .address import Address, AddressGroup, AddressTagging
from .internet_service import InternetService
from .ip_pool import IPPool, IPPoolDynamicMapping
from .ip_pool_group import IPPoolGroup
from .profile_group import ProfileGroup
from .proxy_address import ProxyAddress, ProxyAddressHeaderGroup, ProxyAddressTagging
from .proxy_address_group import ProxyAddressGroup, ProxyAddressGroupTagging
from .service import PORT_RANGE_TYPE, PortRange, ServiceCategory, ServiceCustom, ServiceGroup
from .types import (
    ADDRESS_GROUP_CATEGORY,
    ADDRESS_GROUP_TYPE,
    ADDRESS_TYPE,
    APP_SERVICE_TYPE,
    CHECK_RESET_RANGE,
    CLEARPASS_SPT,
    DIRTY,
    ENABLE_DISABLE,
    HELPER,
    OBJ_TYPE,
    PROTOCOL,
    SDN_ADDR_TYPE,
    SUB_TYPE,
)
from .vip import VIP, VIPDynamicMapping

__all__ = [
    "ADDRESS_GROUP_CATEGORY",
    "ADDRESS_GROUP_TYPE",
    "ADDRESS_TYPE",
    "APP_SERVICE_TYPE",
    "Address",
    "AddressGroup",
    "AddressTagging",
    "CHECK_RESET_RANGE",
    "CLEARPASS_SPT",
    "DIRTY",
    "ENABLE_DISABLE",
    "HELPER",
    "IPPool",
    "IPPoolDynamicMapping",
    "IPPoolGroup",
    "InternetService",
    "OBJ_TYPE",
    "PORT_RANGE_TYPE",
    "PROTOCOL",
    "PortRange",
    "ProfileGroup",
    "ProxyAddress",
    "ProxyAddressGroup",
    "ProxyAddressGroupTagging",
    "ProxyAddressHeaderGroup",
    "ProxyAddressTagging",
    "SDN_ADDR_TYPE",
    "SUB_TYPE",
    "Scope",
    "ServiceCategory",
    "ServiceCustom",
    "ServiceGroup",
    "VIP",
    "VIPDynamicMapping",
]
