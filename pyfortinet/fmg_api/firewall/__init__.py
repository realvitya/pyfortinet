"""Public firewall classes and backwards-compatible explicit type imports."""

from pyfortinet.fmg_api.common import Scope

from .address import Address, AddressGroup, AddressTagging
from .internet_service import InternetService
from .ip_pool import IPPool, IPPoolDynamicMapping
from .ip_pool_group import IPPoolGroup
from .profile_group import ProfileGroup
from .proxy_address import ProxyAddress, ProxyAddressHeaderGroup, ProxyAddressTagging
from .proxy_address_group import ProxyAddressGroup, ProxyAddressGroupTagging
from .service import PORT_RANGE_TYPE as PORT_RANGE_TYPE
from .service import PortRange, ServiceCategory, ServiceCustom, ServiceGroup
from .types import ADDRESS_GROUP_CATEGORY as ADDRESS_GROUP_CATEGORY
from .types import ADDRESS_GROUP_TYPE as ADDRESS_GROUP_TYPE
from .types import ADDRESS_TYPE as ADDRESS_TYPE
from .types import APP_SERVICE_TYPE as APP_SERVICE_TYPE
from .types import CHECK_RESET_RANGE as CHECK_RESET_RANGE
from .types import CLEARPASS_SPT as CLEARPASS_SPT
from .types import DIRTY as DIRTY
from .types import ENABLE_DISABLE as ENABLE_DISABLE
from .types import HELPER as HELPER
from .types import OBJ_TYPE as OBJ_TYPE
from .types import PROTOCOL as PROTOCOL
from .types import SDN_ADDR_TYPE as SDN_ADDR_TYPE
from .types import SUB_TYPE as SUB_TYPE
from .vip import VIP, VIPDynamicMapping

# Wildcard imports expose classes; explicit imports also retain the historical type aliases.
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
