# Addresses and groups

Use an open connection from the [quickstart](../quickstart.md). Run the snippets on this page in order;
write examples require unused names and valid references in your selected ADOM. Await requests
when using an asynchronous client. See the [firewall overview](../firewall_objects.md) for
firmware coverage and shared conventions.

## Address

`Address` represents firewall addresses. Use `subnet` for an IP address or network, `start_ip`
and `end_ip` for a range, or `fqdn` with `type="fqdn"` for a DNS name.

```python
from pyfortinet.fmg_api.firewall import Address

server = Address(name="example-server", subnet="192.0.2.10/32")
network = Address(name="example-network", subnet="192.0.2.0/24")
dns_name = Address(name="example-site", type="fqdn", fqdn="www.example.com")
ip_range = Address(
    name="example-range", type="iprange", start_ip="192.0.2.100", end_ip="192.0.2.110"
)
fmg.add([server, network, dns_name, ip_range])
```

For device-specific overrides, embed another `Address` with `mapping__scope` in
`dynamic_mapping`. See [mapping how-tos](../howto.md#add_or_remove_a_device-specific_address_mapping).
An unnamed `Address` can represent a mapping row; it is not a separate address to add.

## AddressGroup

Members can be existing address/group names or named models. Model references serialize as
names; constructing a member model does not create the member in FortiManager.
This example uses the addresses created above:

```python
from pyfortinet.fmg_api.firewall import AddressGroup

group = AddressGroup(
    name="example-servers",
    member=[server, "example-range"],
    comment="Application servers",
)
fmg.add(group)
```

Remove a group before deleting addresses that it references. Use an explicit empty member list
to clear membership. Groups also support `exclude_member` and embedded `AddressGroup` mappings;
check the reference for fields accepted by the target firmware.

## AddressTagging

`AddressTagging` is embedded metadata, not an independently writable API resource. Its category
is a string and tags are a list. The referenced category and tags must be valid in your ADOM.

```python
from pyfortinet.fmg_api.firewall import Address, AddressTagging

tagged = Address(
    name="example-tagged-server",
    subnet="192.0.2.40/32",
    tagging=[AddressTagging(name="business-role", category="Role", tags=["Backend"])],
)
fmg.add(tagged)
```
