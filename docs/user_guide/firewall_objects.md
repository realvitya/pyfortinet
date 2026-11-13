# Firewall objects

This guide covers every public class exported by `pyfortinet.fmg_api.firewall`, grouped by
purpose. Resource models support high-level operations; helper models are embedded in resource
fields and are not added independently.

Run request examples inside an open connection from the [quickstart](quickstart.md). Examples
with `fmg.add(...)` or `fmg.update(...)` write to the selected ADOM; await those calls with an
asynchronous client. Constructing a model makes no API request and installs no configuration.
Examples in each family build on their preceding snippets. Use unused resource names, and replace
device names, interfaces, profile references, and tagging categories with values in your ADOM.

| Family | Public classes |
| --- | --- |
| Addresses | `Address`, `AddressGroup`, `AddressTagging` |
| Services | `ServiceCategory`, `ServiceCustom`, `PortRange`, `ServiceGroup` |
| Security profiles | `ProfileGroup` |
| Proxy objects | `ProxyAddress`, `ProxyAddressGroup`, `ProxyAddressHeaderGroup` |
| Proxy metadata | `ProxyAddressTagging`, `ProxyAddressGroupTagging` |
| Internet services | `InternetService` |
| Virtual IPs | `VIP`, `VIPDynamicMapping` |
| IP pools | `IPPool`, `IPPoolDynamicMapping`, `IPPoolGroup` |
| Shared mapping helper | `Scope` |

Python field names generally use underscores; serializers write the declared API aliases.
Client writes omit `None` but retain explicit empty lists. Consult the class reference for defaults
that may also be serialized, particularly when making a partial update.

## Firmware coverage

The proxy, Internet service, VIP, and IP pool models follow the supplied **FortiManager 7.6.7
Configuration Database v7.4 ADOM Level Objects** schema. This does not establish the firmware
coverage of every older address, service, or profile field.

The existing verification record reports live FMG 7.4.6 build 2588 checks for five writable
schema-backed resource types and VIP/IPPool mappings. InternetService lookups were skipped
because the lab catalog was empty. FMG 7.6.7 device compatibility remains unverified.
See the [testing guide](../developer_guide/testing.md#additional_firewall_lab_scenarios).
The examples on this page are checked locally; they were not executed against a live device
as part of this documentation update.

## Choose an object family

- [Addresses and groups](firewall/addresses.md)
- [Services](firewall/services.md)
- [Security profiles](firewall/profiles.md)
- [Proxy objects](firewall/proxy.md)
- [Internet services](firewall/internet_services.md)
- [Virtual IPs](firewall/virtual_ips.md)
- [IP pools](firewall/ip_pools.md)
- [Mapping scopes](firewall/mapping_scopes.md)
