"""VIP schema for FMG 7.6.7, FortiOS 7.4 ADOM objects.

Static declarations; no private schema file is needed at runtime.
"""

from typing import Literal, Optional

from pydantic import AliasChoices, BaseModel, Field, field_validator

from pyfortinet.fmg_api import FMGObject
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.firewall._values import as_list, reference_names, uuid_string


class VIPDynamicMappingRealservers(BaseModel):
    """Fields for `pm.config.firewall.vip.dynamic_mapping.realservers`; omitted values are not written."""

    address: Optional[list[str]] = Field(None, description=("Dynamic address of the real server."))
    client_ip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("client-ip", "client_ip"),
        serialization_alias="client-ip",
        description=("Only clients in this IP range can connect to this real server."),
    )
    health_check_proto: Optional[Literal["ping", "http"]] = Field(
        None,
        validation_alias=AliasChoices("health-check-proto", "health_check_proto"),
        serialization_alias="health-check-proto",
    )
    healthcheck: Optional[Literal["disable", "enable", "vip"]] = Field(
        None, description=("Enable to check the responsiveness of the real server before forwarding traffic.")
    )
    holddown_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("holddown-interval", "holddown_interval"),
        serialization_alias="holddown-interval",
        description=(
            "Time in seconds that the system waits before re-activating a previously down active server "
            "in the active-standby mode. This is to prevent any flapping issues."
        ),
    )
    http_host: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("http-host", "http_host"),
        serialization_alias="http-host",
        description=("HTTP server domain name in HTTP header."),
    )
    id: Optional[int] = Field(None, description=("Real server ID."))
    ip: Optional[str] = Field(None, description=("IP address of the real server."))
    max_connections: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("max-connections", "max_connections"),
        serialization_alias="max-connections",
        description=(
            "Max number of active connections that can be directed to the real server. When reached, "
            "sessions are sent to other real servers."
        ),
    )
    monitor: Optional[list[str]] = Field(
        None,
        description=(
            "Name of the health check monitor to use when polling to determine a virtual server's connectivity status."
        ),
    )
    port: Optional[int] = Field(
        None, description=("Port for communicating with the real server. Required if port forwarding is enabled.")
    )
    seq: Optional[int] = Field(None)
    status: Optional[Literal["active", "standby", "disable"]] = Field(
        None,
        description=(
            "Set the status of the real server to active so that it can accept traffic, or on standby "
            "or disabled so no traffic is sent."
        ),
    )
    translate_host: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("translate-host", "translate_host"),
        serialization_alias="translate-host",
        description=("Enable/disable translation of hostname/IP from virtual server to real server."),
    )
    type: Optional[Literal["ip", "address"]] = Field(None, description=("Type of address."))
    verify_cert: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("verify-cert", "verify_cert"),
        serialization_alias="verify-cert",
        description=("Enable/disable certificate verification of the real server."),
    )
    weight: Optional[int] = Field(
        None,
        description=(
            "Weight of the real server. If weighted load balancing is enabled, the server with the "
            "highest weight gets more connections."
        ),
    )

    @field_validator("client_ip", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator("address", "monitor", mode="before")
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)

    @field_validator("translate_host", "verify_cert", mode="before")
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value


class VIPDynamicMappingSslCipherSuites(BaseModel):
    """Fields for `pm.config.firewall.vip.dynamic_mapping.ssl-cipher-suites`; omitted values are not written."""

    cipher: Optional[
        Literal[
            "TLS-RSA-WITH-RC4-128-MD5",
            "TLS-RSA-WITH-RC4-128-SHA",
            "TLS-RSA-WITH-DES-CBC-SHA",
            "TLS-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-RSA-WITH-AES-128-CBC-SHA",
            "TLS-RSA-WITH-AES-256-CBC-SHA",
            "TLS-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-RSA-WITH-AES-256-CBC-SHA256",
            "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-RSA-WITH-SEED-CBC-SHA",
            "TLS-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-DHE-RSA-WITH-DES-CBC-SHA",
            "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-128-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-256-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256",
            "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-DHE-RSA-WITH-SEED-CBC-SHA",
            "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-RC4-128-SHA",
            "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-DHE-DSS-WITH-AES-128-CBC-SHA",
            "TLS-DHE-DSS-WITH-AES-256-CBC-SHA",
            "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256",
            "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256",
            "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384",
            "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA",
            "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384",
            "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384",
            "TLS-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-DHE-DSS-WITH-SEED-CBC-SHA",
            "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA",
            "TLS-DHE-DSS-WITH-DES-CBC-SHA",
            "TLS-AES-128-GCM-SHA256",
            "TLS-AES-256-GCM-SHA384",
            "TLS-CHACHA20-POLY1305-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA",
        ]
    ] = Field(None, description=("Cipher suite name."))
    id: Optional[int] = Field(None)
    priority: Optional[int] = Field(None, description=("SSL/TLS cipher suites priority."))
    versions: Optional[list[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]]] = Field(
        None, description=("SSL/TLS versions that the cipher suite can be used with.")
    )

    @field_validator("versions", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)


class VIPDynamicMapping(BaseModel):
    """Fields for `pm.config.firewall.vip.dynamic_mapping`; omitted values are not written."""

    mapping__scope: Optional[list[Scope]] = Field(
        None, validation_alias=AliasChoices("_scope", "mapping__scope"), serialization_alias="_scope"
    )
    add_nat46_route: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("add-nat46-route", "add_nat46_route"),
        serialization_alias="add-nat46-route",
        description=("Enable/disable adding NAT46 route."),
    )
    arp_reply: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("arp-reply", "arp_reply"),
        serialization_alias="arp-reply",
        description=("Enable to respond to ARP requests for this virtual IP address. Enabled by default."),
    )
    client_cert: Optional[Literal["disable", "enable"]] = Field(
        None, validation_alias=AliasChoices("client-cert", "client_cert"), serialization_alias="client-cert"
    )
    color: Optional[int] = Field(None, description=("Color of icon on the GUI."))
    comment: Optional[str] = Field(None, description=("Comment."))
    dns_mapping_ttl: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("dns-mapping-ttl", "dns_mapping_ttl"),
        serialization_alias="dns-mapping-ttl",
        description=("DNS mapping TTL (Set to zero to use TTL in DNS response, default = 0)."),
    )
    empty_cert_action: Optional[Literal["accept", "block", "accept-unmanageable"]] = Field(
        None,
        validation_alias=AliasChoices("empty-cert-action", "empty_cert_action"),
        serialization_alias="empty-cert-action",
    )
    extaddr: Optional[list[str]] = Field(None, description=("External FQDN address name."))
    extintf: Optional[str] = Field(
        None,
        description=(
            "Interface connected to the source network that receives the packets that will be forwarded "
            "to the destination network."
        ),
    )
    extip: Optional[list[str]] = Field(
        None,
        description=(
            "Support meta variable IP address or address range on the external interface that you want "
            "to map to an address or address range on the destination network."
        ),
    )
    extport: Optional[str] = Field(
        None,
        description=(
            "Support meta variable Incoming port number range that you want to map to a port number "
            "range on the destination network."
        ),
    )
    gratuitous_arp_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("gratuitous-arp-interval", "gratuitous_arp_interval"),
        serialization_alias="gratuitous-arp-interval",
        description=(
            "Enable to have the VIP send gratuitous ARPs. 0=disabled. Set from 5 up to 8640000 seconds to enable."
        ),
    )
    gslb_domain_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("gslb-domain-name", "gslb_domain_name"),
        serialization_alias="gslb-domain-name",
        description=("Domain to use when integrating with FortiGSLB."),
    )
    gslb_hostname: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("gslb-hostname", "gslb_hostname"),
        serialization_alias="gslb-hostname",
        description=("Hostname to use within the configured FortiGSLB domain."),
    )
    h2_support: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("h2-support", "h2_support"),
        serialization_alias="h2-support",
        description=("Enable/disable HTTP2 support (default = enable)."),
    )
    h3_support: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("h3-support", "h3_support"),
        serialization_alias="h3-support",
        description=("Enable/disable HTTP3/QUIC support (default = disable)."),
    )
    http_cookie_age: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-age", "http_cookie_age"),
        serialization_alias="http-cookie-age",
        description=(
            "Time in minutes that client web browsers should keep a cookie. Default is 60 minutes. 0 = no time limit."
        ),
    )
    http_cookie_domain: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-domain", "http_cookie_domain"),
        serialization_alias="http-cookie-domain",
        description=("Domain that HTTP cookie persistence should apply to."),
    )
    http_cookie_domain_from_host: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-domain-from-host", "http_cookie_domain_from_host"),
        serialization_alias="http-cookie-domain-from-host",
        description=("Enable/disable use of HTTP cookie domain from host field in HTTP."),
    )
    http_cookie_generation: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-generation", "http_cookie_generation"),
        serialization_alias="http-cookie-generation",
        description=("Generation of HTTP cookie to be accepted. Changing invalidates all existing cookies."),
    )
    http_cookie_path: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-path", "http_cookie_path"),
        serialization_alias="http-cookie-path",
        description=("Limit HTTP cookie persistence to the specified path."),
    )
    http_cookie_share: Optional[Literal["disable", "same-ip"]] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-share", "http_cookie_share"),
        serialization_alias="http-cookie-share",
        description=(
            "Control sharing of cookies across virtual servers. Use of same-ip means a cookie from one "
            "virtual server can be used by another. Disable stops cookie sharing."
        ),
    )
    http_ip_header: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("http-ip-header", "http_ip_header"),
        serialization_alias="http-ip-header",
        description=(
            "For HTTP multiplexing, enable to add the original client IP address in the XForwarded-For HTTP header."
        ),
    )
    http_ip_header_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("http-ip-header-name", "http_ip_header_name"),
        serialization_alias="http-ip-header-name",
        description=(
            "Support meta variable For HTTP multiplexing, enter a custom HTTPS header name. The "
            "original client IP address is added to this header. If empty, X-Forwarded-For is used."
        ),
    )
    http_multiplex: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("http-multiplex", "http_multiplex"),
        serialization_alias="http-multiplex",
        description=("Enable/disable HTTP multiplexing."),
    )
    http_multiplex_max_concurrent_request: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-multiplex-max-concurrent-request", "http_multiplex_max_concurrent_request"),
        serialization_alias="http-multiplex-max-concurrent-request",
        description=("Maximum number of concurrent requests that a multiplex server can handle (default = unlimited)."),
    )
    http_multiplex_max_request: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-multiplex-max-request", "http_multiplex_max_request"),
        serialization_alias="http-multiplex-max-request",
        description=(
            "Maximum number of requests that a multiplex server can handle before disconnecting "
            "sessions (default = unlimited)."
        ),
    )
    http_multiplex_ttl: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-multiplex-ttl", "http_multiplex_ttl"),
        serialization_alias="http-multiplex-ttl",
        description=("Time-to-live for idle connections to servers."),
    )
    http_redirect: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("http-redirect", "http_redirect"),
        serialization_alias="http-redirect",
        description=("Enable/disable redirection of HTTP to HTTPS."),
    )
    http_supported_max_version: Optional[Literal["http1", "http2"]] = Field(
        None,
        validation_alias=AliasChoices("http-supported-max-version", "http_supported_max_version"),
        serialization_alias="http-supported-max-version",
    )
    https_cookie_secure: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("https-cookie-secure", "https_cookie_secure"),
        serialization_alias="https-cookie-secure",
        description=("Enable/disable verification that inserted HTTPS cookies are secure."),
    )
    id: Optional[int] = Field(None, description=("Custom defined ID."))
    ipv6_mappedip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ipv6-mappedip", "ipv6_mappedip"),
        serialization_alias="ipv6-mappedip",
        description=(
            "Support meta variable Range of mapped IPv6 addresses. Specify the start IPv6 address "
            "followed by a space and the end IPv6 address."
        ),
    )
    ipv6_mappedport: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ipv6-mappedport", "ipv6_mappedport"),
        serialization_alias="ipv6-mappedport",
        description=(
            "Support meta variable IPv6 port number range on the destination network to which the "
            "external port number range is mapped."
        ),
    )
    ldb_method: Optional[
        Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
    ] = Field(
        None,
        validation_alias=AliasChoices("ldb-method", "ldb_method"),
        serialization_alias="ldb-method",
        description=("Method used to distribute sessions to real servers."),
    )
    mapped_addr: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("mapped-addr", "mapped_addr"),
        serialization_alias="mapped-addr",
        description=("Mapped FQDN address name."),
    )
    mappedip: Optional[list[str]] = Field(
        None,
        description=(
            "Support meta variable IP address or address range on the destination network to which the "
            "external IP address is mapped."
        ),
    )
    mappedport: Optional[str] = Field(
        None,
        description=(
            "Support meta variable Port number range on the destination network to which the external "
            "port number range is mapped."
        ),
    )
    max_embryonic_connections: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("max-embryonic-connections", "max_embryonic_connections"),
        serialization_alias="max-embryonic-connections",
        description=("Maximum number of incomplete connections."),
    )
    monitor: Optional[list[str]] = Field(
        None,
        description=(
            "Name of the health check monitor to use when polling to determine a virtual server's connectivity status."
        ),
    )
    nat_source_vip: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("nat-source-vip", "nat_source_vip"),
        serialization_alias="nat-source-vip",
        description=("Enable/disable forcing the source NAT mapped IP to the external IP for all traffic."),
    )
    nat44: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable NAT44."))
    nat46: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable NAT46."))
    one_click_gslb_server: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("one-click-gslb-server", "one_click_gslb_server"),
        serialization_alias="one-click-gslb-server",
        description=("Enable/disable one click GSLB server integration with FortiGSLB."),
    )
    outlook_web_access: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("outlook-web-access", "outlook_web_access"),
        serialization_alias="outlook-web-access",
        description=("Enable to add the Front-End-Https header for Microsoft Outlook Web Access."),
    )
    persistence: Optional[Literal["none", "http-cookie", "ssl-session-id"]] = Field(
        None,
        description=(
            "Configure how to make sure that clients connect to the same server every time they make a "
            "request that is part of the same session."
        ),
    )
    portforward: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable port forwarding."))
    portmapping_type: Optional[Literal["1-to-1", "m-to-n"]] = Field(
        None,
        validation_alias=AliasChoices("portmapping-type", "portmapping_type"),
        serialization_alias="portmapping-type",
        description=("Port mapping type."),
    )
    protocol: Optional[Literal["tcp", "udp", "sctp", "icmp"]] = Field(
        None, description=("Protocol to use when forwarding packets.")
    )
    realservers: Optional[list[VIPDynamicMappingRealservers]] = Field(None)
    server_type: Optional[Literal["http", "https", "ssl", "tcp", "udp", "ip", "imaps", "pop3s", "smtps"]] = Field(
        None,
        validation_alias=AliasChoices("server-type", "server_type"),
        serialization_alias="server-type",
        description=(
            "Protocol to be load balanced by the virtual server (also called the server load balance virtual IP)."
        ),
    )
    service: Optional[list[str]] = Field(None, description=("Service name."))
    src_filter: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("src-filter", "src_filter"),
        serialization_alias="src-filter",
        description=(
            "Support meta variable Source address filter. Each address must be either an IP/subnet "
            "(x.x.x.x/n) or a range (x.x.x.x-y.y.y.y). Separate addresses with spaces."
        ),
    )
    src_vip_filter: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("src-vip-filter", "src_vip_filter"),
        serialization_alias="src-vip-filter",
        description=("Enable/disable use of 'src-filter' to match destinations for the reverse SNAT rule."),
    )
    srcintf_filter: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("srcintf-filter", "srcintf_filter"),
        serialization_alias="srcintf-filter",
        description=("Interfaces to which the VIP applies. Separate the names with spaces."),
    )
    ssl_accept_ffdhe_groups: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-accept-ffdhe-groups", "ssl_accept_ffdhe_groups"),
        serialization_alias="ssl-accept-ffdhe-groups",
        description=("Enable/disable FFDHE cipher suite for SSL key exchange."),
    )
    ssl_algorithm: Optional[Literal["high", "medium", "low", "custom"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-algorithm", "ssl_algorithm"),
        serialization_alias="ssl-algorithm",
        description=("Permitted encryption algorithms for SSL sessions according to encryption strength."),
    )
    ssl_certificate: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ssl-certificate", "ssl_certificate"),
        serialization_alias="ssl-certificate",
        description=("Name of the certificate to use for SSL handshake."),
    )
    ssl_cipher_suites: Optional[list[VIPDynamicMappingSslCipherSuites]] = Field(
        None,
        validation_alias=AliasChoices("ssl-cipher-suites", "ssl_cipher_suites"),
        serialization_alias="ssl-cipher-suites",
    )
    ssl_client_fallback: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-fallback", "ssl_client_fallback"),
        serialization_alias="ssl-client-fallback",
        description=("Enable/disable support for preventing Downgrade Attacks on client connections (RFC 7507)."),
    )
    ssl_client_rekey_count: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-rekey-count", "ssl_client_rekey_count"),
        serialization_alias="ssl-client-rekey-count",
        description=("Maximum length of data in MB before triggering a client rekey (0 = disable)."),
    )
    ssl_client_renegotiation: Optional[Literal["deny", "allow", "secure"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-renegotiation", "ssl_client_renegotiation"),
        serialization_alias="ssl-client-renegotiation",
        description=("Allow, deny, or require secure renegotiation of client sessions to comply with RFC 5746."),
    )
    ssl_client_session_state_max: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-session-state-max", "ssl_client_session_state_max"),
        serialization_alias="ssl-client-session-state-max",
        description=("Maximum number of client to FortiGate SSL session states to keep."),
    )
    ssl_client_session_state_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-session-state-timeout", "ssl_client_session_state_timeout"),
        serialization_alias="ssl-client-session-state-timeout",
        description=("Number of minutes to keep client to FortiGate SSL session state."),
    )
    ssl_client_session_state_type: Optional[Literal["disable", "time", "count", "both"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-session-state-type", "ssl_client_session_state_type"),
        serialization_alias="ssl-client-session-state-type",
        description=(
            "How to expire SSL sessions for the segment of the SSL connection between the client and the FortiGate."
        ),
    )
    ssl_dh_bits: Optional[Literal["768", "1024", "1536", "2048", "3072", "4096"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-dh-bits", "ssl_dh_bits"),
        serialization_alias="ssl-dh-bits",
        description=("Number of bits to use in the Diffie-Hellman exchange for RSA encryption of SSL sessions."),
    )
    ssl_hpkp: Optional[Literal["disable", "enable", "report-only"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp", "ssl_hpkp"),
        serialization_alias="ssl-hpkp",
        description=("Enable/disable including HPKP header in response."),
    )
    ssl_hpkp_age: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-age", "ssl_hpkp_age"),
        serialization_alias="ssl-hpkp-age",
        description=("Number of seconds the client should honor the HPKP setting."),
    )
    ssl_hpkp_backup: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-backup", "ssl_hpkp_backup"),
        serialization_alias="ssl-hpkp-backup",
        description=("Certificate to generate backup HPKP pin from."),
    )
    ssl_hpkp_include_subdomains: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-include-subdomains", "ssl_hpkp_include_subdomains"),
        serialization_alias="ssl-hpkp-include-subdomains",
        description=("Indicate that HPKP header applies to all subdomains."),
    )
    ssl_hpkp_primary: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-primary", "ssl_hpkp_primary"),
        serialization_alias="ssl-hpkp-primary",
        description=("Certificate to generate primary HPKP pin from."),
    )
    ssl_hpkp_report_uri: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-report-uri", "ssl_hpkp_report_uri"),
        serialization_alias="ssl-hpkp-report-uri",
        description=("URL to report HPKP violations to."),
    )
    ssl_hsts: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hsts", "ssl_hsts"),
        serialization_alias="ssl-hsts",
        description=("Enable/disable including HSTS header in response."),
    )
    ssl_hsts_age: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-hsts-age", "ssl_hsts_age"),
        serialization_alias="ssl-hsts-age",
        description=("Number of seconds the client should honor the HSTS setting."),
    )
    ssl_hsts_include_subdomains: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hsts-include-subdomains", "ssl_hsts_include_subdomains"),
        serialization_alias="ssl-hsts-include-subdomains",
        description=("Indicate that HSTS header applies to all subdomains."),
    )
    ssl_http_location_conversion: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-http-location-conversion", "ssl_http_location_conversion"),
        serialization_alias="ssl-http-location-conversion",
        description=("Enable to replace HTTP with HTTPS in the reply's Location HTTP header field."),
    )
    ssl_http_match_host: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-http-match-host", "ssl_http_match_host"),
        serialization_alias="ssl-http-match-host",
        description=("Enable/disable HTTP host matching for location conversion."),
    )
    ssl_max_version: Optional[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-max-version", "ssl_max_version"),
        serialization_alias="ssl-max-version",
        description=("Highest SSL/TLS version acceptable from a client."),
    )
    ssl_min_version: Optional[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-min-version", "ssl_min_version"),
        serialization_alias="ssl-min-version",
        description=("Lowest SSL/TLS version acceptable from a client."),
    )
    ssl_mode: Optional[Literal["half", "full"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-mode", "ssl_mode"),
        serialization_alias="ssl-mode",
        description=(
            "Apply SSL offloading between the client and the FortiGate (half) or from the client to the "
            "FortiGate and from the FortiGate to the server (full)."
        ),
    )
    ssl_pfs: Optional[Literal["require", "deny", "allow"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-pfs", "ssl_pfs"),
        serialization_alias="ssl-pfs",
        description=(
            "Select the cipher suites that can be used for SSL perfect forward secrecy (PFS). Applies "
            "to both client and server sessions."
        ),
    )
    ssl_send_empty_frags: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-send-empty-frags", "ssl_send_empty_frags"),
        serialization_alias="ssl-send-empty-frags",
        description=(
            "Enable/disable sending empty fragments to avoid CBC IV attacks (SSL 3.0 & TLS 1.0 only). "
            "May need to be disabled for compatibility with older systems."
        ),
    )
    ssl_server_algorithm: Optional[Literal["high", "low", "medium", "custom", "client"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-algorithm", "ssl_server_algorithm"),
        serialization_alias="ssl-server-algorithm",
        description=(
            "Permitted encryption algorithms for the server side of SSL full mode sessions according to "
            "encryption strength."
        ),
    )
    ssl_server_max_version: Optional[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "client", "tls-1.3"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-max-version", "ssl_server_max_version"),
        serialization_alias="ssl-server-max-version",
        description=("Highest SSL/TLS version acceptable from a server. Use the client setting by default."),
    )
    ssl_server_min_version: Optional[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "client", "tls-1.3"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-min-version", "ssl_server_min_version"),
        serialization_alias="ssl-server-min-version",
        description=("Lowest SSL/TLS version acceptable from a server. Use the client setting by default."),
    )
    ssl_server_renegotiation: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-renegotiation", "ssl_server_renegotiation"),
        serialization_alias="ssl-server-renegotiation",
        description=("Enable/disable secure renegotiation to comply with RFC 5746."),
    )
    ssl_server_session_state_max: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-session-state-max", "ssl_server_session_state_max"),
        serialization_alias="ssl-server-session-state-max",
        description=("Maximum number of FortiGate to Server SSL session states to keep."),
    )
    ssl_server_session_state_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-session-state-timeout", "ssl_server_session_state_timeout"),
        serialization_alias="ssl-server-session-state-timeout",
        description=("Number of minutes to keep FortiGate to Server SSL session state."),
    )
    ssl_server_session_state_type: Optional[Literal["disable", "time", "count", "both"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-session-state-type", "ssl_server_session_state_type"),
        serialization_alias="ssl-server-session-state-type",
        description=(
            "How to expire SSL sessions for the segment of the SSL connection between the server and the FortiGate."
        ),
    )
    status: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable VIP."))
    type: Optional[
        Literal["static-nat", "load-balance", "server-load-balance", "dns-translation", "fqdn", "access-proxy"]
    ] = Field(
        None,
        description=(
            "Configure a static NAT, load balance, server load balance, access proxy, DNS translation, or FQDN VIP."
        ),
    )
    user_agent_detect: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("user-agent-detect", "user_agent_detect"),
        serialization_alias="user-agent-detect",
    )
    uuid: Optional[str] = Field(
        None, description=("Universally Unique Identifier (UUID; automatically assigned but can be manually reset).")
    )
    vip_id: Optional[int] = Field(None, validation_alias=AliasChoices("vip-id", "vip_id"), serialization_alias="vip-id")
    weblogic_server: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("weblogic-server", "weblogic_server"),
        serialization_alias="weblogic-server",
        description=("Enable to add an HTTP header to indicate SSL offloading for a WebLogic server."),
    )
    websphere_server: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("websphere-server", "websphere_server"),
        serialization_alias="websphere-server",
        description=("Enable to add an HTTP header to indicate SSL offloading for a WebSphere server."),
    )

    @field_validator(
        "mapping__scope",
        "extip",
        "mappedip",
        "realservers",
        "src_filter",
        "srcintf_filter",
        "ssl_cipher_suites",
        mode="before",
    )
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator(
        "extaddr",
        "mapped_addr",
        "monitor",
        "service",
        "ssl_certificate",
        "ssl_hpkp_backup",
        "ssl_hpkp_primary",
        mode="before",
    )
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)

    @field_validator(
        "add_nat46_route",
        "arp_reply",
        "client_cert",
        "h2_support",
        "h3_support",
        "http_cookie_domain_from_host",
        "http_ip_header",
        "http_multiplex",
        "http_redirect",
        "https_cookie_secure",
        "nat_source_vip",
        "nat44",
        "nat46",
        "one_click_gslb_server",
        "outlook_web_access",
        "portforward",
        "src_vip_filter",
        "ssl_accept_ffdhe_groups",
        "ssl_client_fallback",
        "ssl_hpkp_include_subdomains",
        "ssl_hsts",
        "ssl_hsts_include_subdomains",
        "ssl_http_location_conversion",
        "ssl_http_match_host",
        "ssl_send_empty_frags",
        "ssl_server_renegotiation",
        "status",
        "user_agent_detect",
        "weblogic_server",
        "websphere_server",
        mode="before",
    )
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value

    @field_validator("uuid")
    @classmethod
    def normalize_uuid(cls, value: Optional[str]) -> Optional[str]:
        return uuid_string(value)


class VIPGslbPublicIps(BaseModel):
    """Fields for `pm.config.firewall.vip.gslb-public-ips`; omitted values are not written."""

    index: Optional[int] = Field(None, description=("Index of this public IP setting."))
    ip: Optional[str] = Field(None, description=("The publicly accessible IP address."))


class VIPQuic(BaseModel):
    """Fields for `pm.config.firewall.vip.quic`; omitted values are not written."""

    ack_delay_exponent: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ack-delay-exponent", "ack_delay_exponent"),
        serialization_alias="ack-delay-exponent",
        description=("ACK delay exponent (1 - 20, default = 3)."),
    )
    active_connection_id_limit: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("active-connection-id-limit", "active_connection_id_limit"),
        serialization_alias="active-connection-id-limit",
        description=("Active connection ID limit (1 - 8, default = 2)."),
    )
    active_migration: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("active-migration", "active_migration"),
        serialization_alias="active-migration",
        description=("Enable/disable active migration (default = disable)."),
    )
    grease_quic_bit: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("grease-quic-bit", "grease_quic_bit"),
        serialization_alias="grease-quic-bit",
        description=("Enable/disable grease QUIC bit (default = enable)."),
    )
    max_ack_delay: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("max-ack-delay", "max_ack_delay"),
        serialization_alias="max-ack-delay",
        description=("Maximum ACK delay in milliseconds (1 - 16383, default = 25)."),
    )
    max_datagram_frame_size: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("max-datagram-frame-size", "max_datagram_frame_size"),
        serialization_alias="max-datagram-frame-size",
        description=("Maximum datagram frame size in bytes (1 - 1500, default = 1500)."),
    )
    max_idle_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("max-idle-timeout", "max_idle_timeout"),
        serialization_alias="max-idle-timeout",
        description=("Maximum idle timeout milliseconds (1 - 60000, default = 30000)."),
    )
    max_udp_payload_size: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("max-udp-payload-size", "max_udp_payload_size"),
        serialization_alias="max-udp-payload-size",
        description=("Maximum UDP payload size in bytes (1200 - 1500, default = 1500)."),
    )

    @field_validator("active_migration", "grease_quic_bit", mode="before")
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value


class VIPRealservers(BaseModel):
    """Fields for `pm.config.firewall.vip.realservers`; omitted values are not written."""

    address: Optional[list[str]] = Field(None, description=("Dynamic address of the real server."))
    client_ip: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("client-ip", "client_ip"),
        serialization_alias="client-ip",
        description=("Only clients in this IP range can connect to this real server."),
    )
    healthcheck: Optional[Literal["disable", "enable", "vip"]] = Field(
        None, description=("Enable to check the responsiveness of the real server before forwarding traffic.")
    )
    holddown_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("holddown-interval", "holddown_interval"),
        serialization_alias="holddown-interval",
        description=(
            "Time in seconds that the system waits before re-activating a previously down active server "
            "in the active-standby mode. This is to prevent any flapping issues."
        ),
    )
    http_host: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("http-host", "http_host"),
        serialization_alias="http-host",
        description=("HTTP server domain name in HTTP header."),
    )
    id: Optional[int] = Field(None, description=("Real server ID."))
    ip: Optional[str] = Field(None, description=("IP address of the real server."))
    max_connections: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("max-connections", "max_connections"),
        serialization_alias="max-connections",
        description=(
            "Max number of active connections that can be directed to the real server. When reached, "
            "sessions are sent to other real servers."
        ),
    )
    monitor: Optional[list[str]] = Field(
        None,
        description=(
            "Name of the health check monitor to use when polling to determine a virtual server's connectivity status."
        ),
    )
    port: Optional[int] = Field(
        None, description=("Port for communicating with the real server. Required if port forwarding is enabled.")
    )
    status: Optional[Literal["active", "standby", "disable"]] = Field(
        None,
        description=(
            "Set the status of the real server to active so that it can accept traffic, or on standby "
            "or disabled so no traffic is sent."
        ),
    )
    translate_host: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("translate-host", "translate_host"),
        serialization_alias="translate-host",
        description=("Enable/disable translation of hostname/IP from virtual server to real server."),
    )
    type: Optional[Literal["ip", "address"]] = Field(None, description=("Type of address."))
    verify_cert: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("verify-cert", "verify_cert"),
        serialization_alias="verify-cert",
        description=("Enable/disable certificate verification of the real server."),
    )
    weight: Optional[int] = Field(
        None,
        description=(
            "Weight of the real server. If weighted load balancing is enabled, the server with the "
            "highest weight gets more connections."
        ),
    )

    @field_validator("client_ip", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator("address", "monitor", mode="before")
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)

    @field_validator("translate_host", "verify_cert", mode="before")
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value


class VIPSslCipherSuites(BaseModel):
    """Fields for `pm.config.firewall.vip.ssl-cipher-suites`; omitted values are not written."""

    cipher: Optional[
        Literal[
            "TLS-RSA-WITH-RC4-128-MD5",
            "TLS-RSA-WITH-RC4-128-SHA",
            "TLS-RSA-WITH-DES-CBC-SHA",
            "TLS-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-RSA-WITH-AES-128-CBC-SHA",
            "TLS-RSA-WITH-AES-256-CBC-SHA",
            "TLS-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-RSA-WITH-AES-256-CBC-SHA256",
            "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-RSA-WITH-SEED-CBC-SHA",
            "TLS-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-DHE-RSA-WITH-DES-CBC-SHA",
            "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-128-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-256-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256",
            "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-DHE-RSA-WITH-SEED-CBC-SHA",
            "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-RC4-128-SHA",
            "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-DHE-DSS-WITH-AES-128-CBC-SHA",
            "TLS-DHE-DSS-WITH-AES-256-CBC-SHA",
            "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256",
            "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256",
            "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384",
            "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA",
            "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384",
            "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384",
            "TLS-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-DHE-DSS-WITH-SEED-CBC-SHA",
            "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA",
            "TLS-DHE-DSS-WITH-DES-CBC-SHA",
            "TLS-AES-128-GCM-SHA256",
            "TLS-AES-256-GCM-SHA384",
            "TLS-CHACHA20-POLY1305-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA",
        ]
    ] = Field(None, description=("Cipher suite name."))
    priority: Optional[int] = Field(None, description=("SSL/TLS cipher suites priority."))
    versions: Optional[list[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]]] = Field(
        None, description=("SSL/TLS versions that the cipher suite can be used with.")
    )

    @field_validator("versions", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)


class VIPSslServerCipherSuites(BaseModel):
    """Fields for `pm.config.firewall.vip.ssl-server-cipher-suites`; omitted values are not written."""

    cipher: Optional[
        Literal[
            "TLS-RSA-WITH-RC4-128-MD5",
            "TLS-RSA-WITH-RC4-128-SHA",
            "TLS-RSA-WITH-DES-CBC-SHA",
            "TLS-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-RSA-WITH-AES-128-CBC-SHA",
            "TLS-RSA-WITH-AES-256-CBC-SHA",
            "TLS-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-RSA-WITH-AES-256-CBC-SHA256",
            "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-RSA-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-RSA-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-RSA-WITH-SEED-CBC-SHA",
            "TLS-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-DHE-RSA-WITH-DES-CBC-SHA",
            "TLS-DHE-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-128-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-256-CBC-SHA",
            "TLS-DHE-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-AES-256-CBC-SHA256",
            "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-DHE-RSA-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-DHE-RSA-WITH-SEED-CBC-SHA",
            "TLS-DHE-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-DHE-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-RC4-128-SHA",
            "TLS-ECDHE-RSA-WITH-3DES-EDE-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA",
            "TLS-ECDHE-RSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-ECDHE-ECDSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-DHE-RSA-WITH-CHACHA20-POLY1305-SHA256",
            "TLS-DHE-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-DHE-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-DHE-DSS-WITH-AES-128-CBC-SHA",
            "TLS-DHE-DSS-WITH-AES-256-CBC-SHA",
            "TLS-DHE-DSS-WITH-AES-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-AES-128-GCM-SHA256",
            "TLS-DHE-DSS-WITH-AES-256-CBC-SHA256",
            "TLS-DHE-DSS-WITH-AES-256-GCM-SHA384",
            "TLS-ECDHE-RSA-WITH-AES-128-CBC-SHA256",
            "TLS-ECDHE-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-ECDHE-RSA-WITH-AES-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA",
            "TLS-ECDHE-ECDSA-WITH-AES-128-CBC-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-128-GCM-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA384",
            "TLS-ECDHE-ECDSA-WITH-AES-256-GCM-SHA384",
            "TLS-RSA-WITH-AES-128-GCM-SHA256",
            "TLS-RSA-WITH-AES-256-GCM-SHA384",
            "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA",
            "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA",
            "TLS-DHE-DSS-WITH-CAMELLIA-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-CAMELLIA-256-CBC-SHA256",
            "TLS-DHE-DSS-WITH-SEED-CBC-SHA",
            "TLS-DHE-DSS-WITH-ARIA-128-CBC-SHA256",
            "TLS-DHE-DSS-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-RSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-ECDHE-RSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-ECDHE-ECDSA-WITH-ARIA-128-CBC-SHA256",
            "TLS-ECDHE-ECDSA-WITH-ARIA-256-CBC-SHA384",
            "TLS-DHE-DSS-WITH-3DES-EDE-CBC-SHA",
            "TLS-DHE-DSS-WITH-DES-CBC-SHA",
            "TLS-AES-128-GCM-SHA256",
            "TLS-AES-256-GCM-SHA384",
            "TLS-CHACHA20-POLY1305-SHA256",
            "TLS-ECDHE-ECDSA-WITH-AES-256-CBC-SHA",
        ]
    ] = Field(None, description=("Cipher suite name."))
    priority: Optional[int] = Field(None, description=("SSL/TLS cipher suites priority."))
    versions: Optional[list[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]]] = Field(
        None, description=("SSL/TLS versions that the cipher suite can be used with.")
    )

    @field_validator("versions", mode="before")
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)


class VIP(FMGObject):
    """Fields for `pm.config.firewall.vip`; omitted values are not written."""

    _url: str = "/pm/config/{scope}/obj/firewall/vip/{vip}"
    _master_keys = {"vip": "name"}

    add_nat46_route: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("add-nat46-route", "add_nat46_route"),
        serialization_alias="add-nat46-route",
        description=("Enable/disable adding NAT46 route."),
    )
    arp_reply: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("arp-reply", "arp_reply"),
        serialization_alias="arp-reply",
        description=("Enable to respond to ARP requests for this virtual IP address. Enabled by default."),
    )
    color: Optional[int] = Field(None, description=("Color of icon on the GUI."))
    comment: Optional[str] = Field(None, description=("Comment."))
    dns_mapping_ttl: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("dns-mapping-ttl", "dns_mapping_ttl"),
        serialization_alias="dns-mapping-ttl",
        description=("DNS mapping TTL (Set to zero to use TTL in DNS response, default = 0)."),
    )
    dynamic_mapping: Optional[list[VIPDynamicMapping]] = Field(None)
    extaddr: Optional[list[str]] = Field(None, description=("External FQDN address name."))
    extintf: Optional[list[str]] = Field(
        None,
        description=(
            "Interface connected to the source network that receives the packets that will be forwarded "
            "to the destination network."
        ),
    )
    extip: Optional[list[str]] = Field(
        None,
        description=(
            "Support meta variable IP address or address range on the external interface that you want "
            "to map to an address or address range on the destination network."
        ),
    )
    extport: Optional[str] = Field(
        None,
        description=(
            "Support meta variable Incoming port number range that you want to map to a port number "
            "range on the destination network."
        ),
    )
    gratuitous_arp_interval: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("gratuitous-arp-interval", "gratuitous_arp_interval"),
        serialization_alias="gratuitous-arp-interval",
        description=(
            "Enable to have the VIP send gratuitous ARPs. 0=disabled. Set from 5 up to 8640000 seconds to enable."
        ),
    )
    gslb_domain_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("gslb-domain-name", "gslb_domain_name"),
        serialization_alias="gslb-domain-name",
        description=("Domain to use when integrating with FortiGSLB."),
    )
    gslb_hostname: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("gslb-hostname", "gslb_hostname"),
        serialization_alias="gslb-hostname",
        description=("Hostname to use within the configured FortiGSLB domain."),
    )
    gslb_public_ips: Optional[list[VIPGslbPublicIps]] = Field(
        None, validation_alias=AliasChoices("gslb-public-ips", "gslb_public_ips"), serialization_alias="gslb-public-ips"
    )
    h2_support: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("h2-support", "h2_support"),
        serialization_alias="h2-support",
        description=("Enable/disable HTTP2 support (default = enable)."),
    )
    h3_support: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("h3-support", "h3_support"),
        serialization_alias="h3-support",
        description=("Enable/disable HTTP3/QUIC support (default = disable)."),
    )
    http_cookie_age: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-age", "http_cookie_age"),
        serialization_alias="http-cookie-age",
        description=(
            "Time in minutes that client web browsers should keep a cookie. Default is 60 minutes. 0 = no time limit."
        ),
    )
    http_cookie_domain: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-domain", "http_cookie_domain"),
        serialization_alias="http-cookie-domain",
        description=("Domain that HTTP cookie persistence should apply to."),
    )
    http_cookie_domain_from_host: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-domain-from-host", "http_cookie_domain_from_host"),
        serialization_alias="http-cookie-domain-from-host",
        description=("Enable/disable use of HTTP cookie domain from host field in HTTP."),
    )
    http_cookie_generation: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-generation", "http_cookie_generation"),
        serialization_alias="http-cookie-generation",
        description=("Generation of HTTP cookie to be accepted. Changing invalidates all existing cookies."),
    )
    http_cookie_path: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-path", "http_cookie_path"),
        serialization_alias="http-cookie-path",
        description=("Limit HTTP cookie persistence to the specified path."),
    )
    http_cookie_share: Optional[Literal["disable", "same-ip"]] = Field(
        None,
        validation_alias=AliasChoices("http-cookie-share", "http_cookie_share"),
        serialization_alias="http-cookie-share",
        description=(
            "Control sharing of cookies across virtual servers. Use of same-ip means a cookie from one "
            "virtual server can be used by another. Disable stops cookie sharing."
        ),
    )
    http_ip_header: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("http-ip-header", "http_ip_header"),
        serialization_alias="http-ip-header",
        description=(
            "For HTTP multiplexing, enable to add the original client IP address in the XForwarded-For HTTP header."
        ),
    )
    http_ip_header_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("http-ip-header-name", "http_ip_header_name"),
        serialization_alias="http-ip-header-name",
        description=(
            "Support meta variable For HTTP multiplexing, enter a custom HTTPS header name. The "
            "original client IP address is added to this header. If empty, X-Forwarded-For is used."
        ),
    )
    http_multiplex: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("http-multiplex", "http_multiplex"),
        serialization_alias="http-multiplex",
        description=("Enable/disable HTTP multiplexing."),
    )
    http_multiplex_max_concurrent_request: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-multiplex-max-concurrent-request", "http_multiplex_max_concurrent_request"),
        serialization_alias="http-multiplex-max-concurrent-request",
        description=("Maximum number of concurrent requests that a multiplex server can handle (default = unlimited)."),
    )
    http_multiplex_max_request: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-multiplex-max-request", "http_multiplex_max_request"),
        serialization_alias="http-multiplex-max-request",
        description=(
            "Maximum number of requests that a multiplex server can handle before disconnecting "
            "sessions (default = unlimited)."
        ),
    )
    http_multiplex_ttl: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("http-multiplex-ttl", "http_multiplex_ttl"),
        serialization_alias="http-multiplex-ttl",
        description=("Time-to-live for idle connections to servers."),
    )
    http_redirect: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("http-redirect", "http_redirect"),
        serialization_alias="http-redirect",
        description=("Enable/disable redirection of HTTP to HTTPS."),
    )
    https_cookie_secure: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("https-cookie-secure", "https_cookie_secure"),
        serialization_alias="https-cookie-secure",
        description=("Enable/disable verification that inserted HTTPS cookies are secure."),
    )
    id: Optional[int] = Field(None, description=("Custom defined ID."))
    ipv6_mappedip: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ipv6-mappedip", "ipv6_mappedip"),
        serialization_alias="ipv6-mappedip",
        description=(
            "Support meta variable Range of mapped IPv6 addresses. Specify the start IPv6 address "
            "followed by a space and the end IPv6 address."
        ),
    )
    ipv6_mappedport: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ipv6-mappedport", "ipv6_mappedport"),
        serialization_alias="ipv6-mappedport",
        description=(
            "Support meta variable IPv6 port number range on the destination network to which the "
            "external port number range is mapped."
        ),
    )
    ldb_method: Optional[
        Literal["static", "round-robin", "weighted", "least-session", "least-rtt", "first-alive", "http-host"]
    ] = Field(
        None,
        validation_alias=AliasChoices("ldb-method", "ldb_method"),
        serialization_alias="ldb-method",
        description=("Method used to distribute sessions to real servers."),
    )
    mapped_addr: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("mapped-addr", "mapped_addr"),
        serialization_alias="mapped-addr",
        description=("Mapped FQDN address name."),
    )
    mappedip: Optional[list[str]] = Field(
        None,
        description=(
            "Support meta variable IP address or address range on the destination network to which the "
            "external IP address is mapped."
        ),
    )
    mappedport: Optional[str] = Field(
        None,
        description=(
            "Support meta variable Port number range on the destination network to which the external "
            "port number range is mapped."
        ),
    )
    max_embryonic_connections: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("max-embryonic-connections", "max_embryonic_connections"),
        serialization_alias="max-embryonic-connections",
        description=("Maximum number of incomplete connections."),
    )
    monitor: Optional[list[str]] = Field(
        None,
        description=(
            "Name of the health check monitor to use when polling to determine a virtual server's connectivity status."
        ),
    )
    name: Optional[str] = Field(None, description=("Virtual IP name."))
    nat_source_vip: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("nat-source-vip", "nat_source_vip"),
        serialization_alias="nat-source-vip",
        description=("Enable/disable forcing the source NAT mapped IP to the external IP for all traffic."),
    )
    nat44: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable NAT44."))
    nat46: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable NAT46."))
    one_click_gslb_server: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("one-click-gslb-server", "one_click_gslb_server"),
        serialization_alias="one-click-gslb-server",
        description=("Enable/disable one click GSLB server integration with FortiGSLB."),
    )
    outlook_web_access: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("outlook-web-access", "outlook_web_access"),
        serialization_alias="outlook-web-access",
        description=("Enable to add the Front-End-Https header for Microsoft Outlook Web Access."),
    )
    persistence: Optional[Literal["none", "http-cookie", "ssl-session-id"]] = Field(
        None,
        description=(
            "Configure how to make sure that clients connect to the same server every time they make a "
            "request that is part of the same session."
        ),
    )
    portforward: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable port forwarding."))
    portmapping_type: Optional[Literal["1-to-1", "m-to-n"]] = Field(
        None,
        validation_alias=AliasChoices("portmapping-type", "portmapping_type"),
        serialization_alias="portmapping-type",
        description=("Port mapping type."),
    )
    protocol: Optional[Literal["tcp", "udp", "sctp", "icmp"]] = Field(
        None, description=("Protocol to use when forwarding packets.")
    )
    quic: Optional[VIPQuic] = Field(None)
    realservers: Optional[list[VIPRealservers]] = Field(None)
    server_type: Optional[Literal["http", "https", "ssl", "tcp", "udp", "ip", "imaps", "pop3s", "smtps"]] = Field(
        None,
        validation_alias=AliasChoices("server-type", "server_type"),
        serialization_alias="server-type",
        description=(
            "Protocol to be load balanced by the virtual server (also called the server load balance virtual IP)."
        ),
    )
    service: Optional[list[str]] = Field(None, description=("Service name."))
    src_filter: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("src-filter", "src_filter"),
        serialization_alias="src-filter",
        description=(
            "Support meta variable Source address filter. Each address must be either an IP/subnet "
            "(x.x.x.x/n) or a range (x.x.x.x-y.y.y.y). Separate addresses with spaces."
        ),
    )
    src_vip_filter: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("src-vip-filter", "src_vip_filter"),
        serialization_alias="src-vip-filter",
        description=("Enable/disable use of 'src-filter' to match destinations for the reverse SNAT rule."),
    )
    srcintf_filter: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("srcintf-filter", "srcintf_filter"),
        serialization_alias="srcintf-filter",
        description=("Interfaces to which the VIP applies. Separate the names with spaces."),
    )
    ssl_accept_ffdhe_groups: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-accept-ffdhe-groups", "ssl_accept_ffdhe_groups"),
        serialization_alias="ssl-accept-ffdhe-groups",
        description=("Enable/disable FFDHE cipher suite for SSL key exchange."),
    )
    ssl_algorithm: Optional[Literal["high", "medium", "low", "custom"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-algorithm", "ssl_algorithm"),
        serialization_alias="ssl-algorithm",
        description=("Permitted encryption algorithms for SSL sessions according to encryption strength."),
    )
    ssl_certificate: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ssl-certificate", "ssl_certificate"),
        serialization_alias="ssl-certificate",
        description=("Name of the certificate to use for SSL handshake."),
    )
    ssl_cipher_suites: Optional[list[VIPSslCipherSuites]] = Field(
        None,
        validation_alias=AliasChoices("ssl-cipher-suites", "ssl_cipher_suites"),
        serialization_alias="ssl-cipher-suites",
    )
    ssl_client_fallback: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-fallback", "ssl_client_fallback"),
        serialization_alias="ssl-client-fallback",
        description=("Enable/disable support for preventing Downgrade Attacks on client connections (RFC 7507)."),
    )
    ssl_client_rekey_count: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-rekey-count", "ssl_client_rekey_count"),
        serialization_alias="ssl-client-rekey-count",
        description=("Maximum length of data in MB before triggering a client rekey (0 = disable)."),
    )
    ssl_client_renegotiation: Optional[Literal["deny", "allow", "secure"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-renegotiation", "ssl_client_renegotiation"),
        serialization_alias="ssl-client-renegotiation",
        description=("Allow, deny, or require secure renegotiation of client sessions to comply with RFC 5746."),
    )
    ssl_client_session_state_max: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-session-state-max", "ssl_client_session_state_max"),
        serialization_alias="ssl-client-session-state-max",
        description=("Maximum number of client to FortiGate SSL session states to keep."),
    )
    ssl_client_session_state_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-session-state-timeout", "ssl_client_session_state_timeout"),
        serialization_alias="ssl-client-session-state-timeout",
        description=("Number of minutes to keep client to FortiGate SSL session state."),
    )
    ssl_client_session_state_type: Optional[Literal["disable", "time", "count", "both"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-client-session-state-type", "ssl_client_session_state_type"),
        serialization_alias="ssl-client-session-state-type",
        description=(
            "How to expire SSL sessions for the segment of the SSL connection between the client and the FortiGate."
        ),
    )
    ssl_dh_bits: Optional[Literal["768", "1024", "1536", "2048", "3072", "4096"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-dh-bits", "ssl_dh_bits"),
        serialization_alias="ssl-dh-bits",
        description=("Number of bits to use in the Diffie-Hellman exchange for RSA encryption of SSL sessions."),
    )
    ssl_hpkp: Optional[Literal["disable", "enable", "report-only"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp", "ssl_hpkp"),
        serialization_alias="ssl-hpkp",
        description=("Enable/disable including HPKP header in response."),
    )
    ssl_hpkp_age: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-age", "ssl_hpkp_age"),
        serialization_alias="ssl-hpkp-age",
        description=("Number of seconds the client should honor the HPKP setting."),
    )
    ssl_hpkp_backup: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-backup", "ssl_hpkp_backup"),
        serialization_alias="ssl-hpkp-backup",
        description=("Certificate to generate backup HPKP pin from."),
    )
    ssl_hpkp_include_subdomains: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-include-subdomains", "ssl_hpkp_include_subdomains"),
        serialization_alias="ssl-hpkp-include-subdomains",
        description=("Indicate that HPKP header applies to all subdomains."),
    )
    ssl_hpkp_primary: Optional[list[str]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-primary", "ssl_hpkp_primary"),
        serialization_alias="ssl-hpkp-primary",
        description=("Certificate to generate primary HPKP pin from."),
    )
    ssl_hpkp_report_uri: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("ssl-hpkp-report-uri", "ssl_hpkp_report_uri"),
        serialization_alias="ssl-hpkp-report-uri",
        description=("URL to report HPKP violations to."),
    )
    ssl_hsts: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hsts", "ssl_hsts"),
        serialization_alias="ssl-hsts",
        description=("Enable/disable including HSTS header in response."),
    )
    ssl_hsts_age: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-hsts-age", "ssl_hsts_age"),
        serialization_alias="ssl-hsts-age",
        description=("Number of seconds the client should honor the HSTS setting."),
    )
    ssl_hsts_include_subdomains: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-hsts-include-subdomains", "ssl_hsts_include_subdomains"),
        serialization_alias="ssl-hsts-include-subdomains",
        description=("Indicate that HSTS header applies to all subdomains."),
    )
    ssl_http_location_conversion: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-http-location-conversion", "ssl_http_location_conversion"),
        serialization_alias="ssl-http-location-conversion",
        description=("Enable to replace HTTP with HTTPS in the reply's Location HTTP header field."),
    )
    ssl_http_match_host: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-http-match-host", "ssl_http_match_host"),
        serialization_alias="ssl-http-match-host",
        description=("Enable/disable HTTP host matching for location conversion."),
    )
    ssl_max_version: Optional[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-max-version", "ssl_max_version"),
        serialization_alias="ssl-max-version",
        description=("Highest SSL/TLS version acceptable from a client."),
    )
    ssl_min_version: Optional[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "tls-1.3"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-min-version", "ssl_min_version"),
        serialization_alias="ssl-min-version",
        description=("Lowest SSL/TLS version acceptable from a client."),
    )
    ssl_mode: Optional[Literal["half", "full"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-mode", "ssl_mode"),
        serialization_alias="ssl-mode",
        description=(
            "Apply SSL offloading between the client and the FortiGate (half) or from the client to the "
            "FortiGate and from the FortiGate to the server (full)."
        ),
    )
    ssl_pfs: Optional[Literal["require", "deny", "allow"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-pfs", "ssl_pfs"),
        serialization_alias="ssl-pfs",
        description=(
            "Select the cipher suites that can be used for SSL perfect forward secrecy (PFS). Applies "
            "to both client and server sessions."
        ),
    )
    ssl_send_empty_frags: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-send-empty-frags", "ssl_send_empty_frags"),
        serialization_alias="ssl-send-empty-frags",
        description=(
            "Enable/disable sending empty fragments to avoid CBC IV attacks (SSL 3.0 & TLS 1.0 only). "
            "May need to be disabled for compatibility with older systems."
        ),
    )
    ssl_server_algorithm: Optional[Literal["high", "low", "medium", "custom", "client"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-algorithm", "ssl_server_algorithm"),
        serialization_alias="ssl-server-algorithm",
        description=(
            "Permitted encryption algorithms for the server side of SSL full mode sessions according to "
            "encryption strength."
        ),
    )
    ssl_server_cipher_suites: Optional[list[VIPSslServerCipherSuites]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-cipher-suites", "ssl_server_cipher_suites"),
        serialization_alias="ssl-server-cipher-suites",
    )
    ssl_server_max_version: Optional[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "client", "tls-1.3"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-max-version", "ssl_server_max_version"),
        serialization_alias="ssl-server-max-version",
        description=("Highest SSL/TLS version acceptable from a server. Use the client setting by default."),
    )
    ssl_server_min_version: Optional[Literal["ssl-3.0", "tls-1.0", "tls-1.1", "tls-1.2", "client", "tls-1.3"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-min-version", "ssl_server_min_version"),
        serialization_alias="ssl-server-min-version",
        description=("Lowest SSL/TLS version acceptable from a server. Use the client setting by default."),
    )
    ssl_server_renegotiation: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-renegotiation", "ssl_server_renegotiation"),
        serialization_alias="ssl-server-renegotiation",
        description=("Enable/disable secure renegotiation to comply with RFC 5746."),
    )
    ssl_server_session_state_max: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-session-state-max", "ssl_server_session_state_max"),
        serialization_alias="ssl-server-session-state-max",
        description=("Maximum number of FortiGate to Server SSL session states to keep."),
    )
    ssl_server_session_state_timeout: Optional[int] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-session-state-timeout", "ssl_server_session_state_timeout"),
        serialization_alias="ssl-server-session-state-timeout",
        description=("Number of minutes to keep FortiGate to Server SSL session state."),
    )
    ssl_server_session_state_type: Optional[Literal["disable", "time", "count", "both"]] = Field(
        None,
        validation_alias=AliasChoices("ssl-server-session-state-type", "ssl_server_session_state_type"),
        serialization_alias="ssl-server-session-state-type",
        description=(
            "How to expire SSL sessions for the segment of the SSL connection between the server and the FortiGate."
        ),
    )
    status: Optional[Literal["disable", "enable"]] = Field(None, description=("Enable/disable VIP."))
    type: Optional[
        Literal["static-nat", "load-balance", "server-load-balance", "dns-translation", "fqdn", "access-proxy"]
    ] = Field(
        None,
        description=(
            "Configure a static NAT, load balance, server load balance, access proxy, DNS translation, or FQDN VIP."
        ),
    )
    uuid: Optional[str] = Field(
        None, description=("Universally Unique Identifier (UUID; automatically assigned but can be manually reset).")
    )
    weblogic_server: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("weblogic-server", "weblogic_server"),
        serialization_alias="weblogic-server",
        description=("Enable to add an HTTP header to indicate SSL offloading for a WebLogic server."),
    )
    websphere_server: Optional[Literal["disable", "enable"]] = Field(
        None,
        validation_alias=AliasChoices("websphere-server", "websphere_server"),
        serialization_alias="websphere-server",
        description=("Enable to add an HTTP header to indicate SSL offloading for a WebSphere server."),
    )

    @field_validator(
        "dynamic_mapping",
        "extip",
        "gslb_public_ips",
        "mappedip",
        "realservers",
        "src_filter",
        "ssl_cipher_suites",
        "ssl_server_cipher_suites",
        mode="before",
    )
    @classmethod
    def normalize_as_list(cls, value: object) -> Optional[list[object]]:
        return as_list(value)

    @field_validator(
        "extaddr",
        "extintf",
        "mapped_addr",
        "monitor",
        "service",
        "srcintf_filter",
        "ssl_certificate",
        "ssl_hpkp_backup",
        "ssl_hpkp_primary",
        mode="before",
    )
    @classmethod
    def normalize_reference_names(cls, value: object) -> Optional[list[str]]:
        return reference_names(value)

    @field_validator(
        "add_nat46_route",
        "arp_reply",
        "h2_support",
        "h3_support",
        "http_cookie_domain_from_host",
        "http_ip_header",
        "http_multiplex",
        "http_redirect",
        "https_cookie_secure",
        "nat_source_vip",
        "nat44",
        "nat46",
        "one_click_gslb_server",
        "outlook_web_access",
        "portforward",
        "src_vip_filter",
        "ssl_accept_ffdhe_groups",
        "ssl_client_fallback",
        "ssl_hpkp_include_subdomains",
        "ssl_hsts",
        "ssl_hsts_include_subdomains",
        "ssl_http_location_conversion",
        "ssl_http_match_host",
        "ssl_send_empty_frags",
        "ssl_server_renegotiation",
        "status",
        "weblogic_server",
        "websphere_server",
        mode="before",
    )
    @classmethod
    def normalize_switch(cls, value: object) -> object:
        if isinstance(value, int) and value in (0, 1):
            return ("disable", "enable")[value]
        return value

    @field_validator("uuid")
    @classmethod
    def normalize_uuid(cls, value: Optional[str]) -> Optional[str]:
        return uuid_string(value)
