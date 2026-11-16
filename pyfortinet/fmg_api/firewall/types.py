"""Literal choices shared by the firewall models."""

from typing import Literal

ADDRESS_GROUP_TYPE = Literal["default", "array", "folder"]
ADDRESS_GROUP_CATEGORY = Literal["default", "ztna-ems-tag", "ztna-geo-tag"]
ENABLE_DISABLE = Literal["disable", "enable"]
ADDRESS_TYPE = Literal[
    "ipmask",
    "iprange",
    "fqdn",
    "wildcard",
    "geography",
    "url",
    "wildcard-fqdn",
    "nsx",
    "aws",
    "dynamic",
    "interface-subnet",
    "mac",
    "fqdn-group",
]
CLEARPASS_SPT = Literal["unknown", "healthy", "quarantine", "checkup", "transition", "infected", "transient"]
DIRTY = Literal["dirty", "clean"]
OBJ_TYPE = Literal["ip", "mac"]
SDN_ADDR_TYPE = Literal["private", "public", "all"]
SUB_TYPE = Literal[
    "sdn", "clearpass-spt", "fsso", "ems-tag", "swc-tag", "fortivoice-tag", "fortinac-tag", "fortipolicy-tag"
]
APP_SERVICE_TYPE = Literal["disable", "app-id", "app-category"]
CHECK_RESET_RANGE = Literal["disable", "default", "strict"]
HELPER = Literal[
    "disable",
    "auto",
    "ftp",
    "tftp",
    "ras",
    "h323",
    "tns",
    "mms",
    "sip",
    "pptp",
    "rtsp",
    "dns-udp",
    "dns-tcp",
    "pmap",
    "rsh",
    "dcerpc",
    "mgcp",
    "gtp-c",
    "gtp-u",
    "gtp-b",
    "pfcp",
]
PROTOCOL = Literal[
    "ICMP", "IP", "TCP/UDP/SCTP", "ICMP6", "HTTP", "FTP", "CONNECT", "SOCKS", "ALL", "SOCKS-TCP", "SOCKS-UDP"
]
