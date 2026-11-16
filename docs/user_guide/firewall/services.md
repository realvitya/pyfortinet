# Services

Use an open connection from the [quickstart](../quickstart.md). Run the snippets on this page in order;
write examples require unused names and valid references in your selected ADOM. Await requests
when using an asynchronous client. See the [firewall overview](../firewall_objects.md) for
firmware coverage and shared conventions.

## ServiceCategory

Create categories before custom services that reference them:

```python
from pyfortinet.fmg_api.firewall import ServiceCategory

category = ServiceCategory(name="Example applications", comment="Application service definitions")
fmg.add(category)
```

## ServiceCustom

`ServiceCustom` models TCP, UDP, SCTP, ICMP, and other supported service definitions. Categories
can be names or `ServiceCategory` instances. The category in this example was created above.

```python
from pyfortinet.fmg_api.firewall import ServiceCustom

web = ServiceCustom(
    name="example-web",
    protocol="TCP/UDP/SCTP",
    category=[category],
    tcp_portrange=["443", "8443"],
)
dns = ServiceCustom(
    name="example-dns",
    protocol="TCP/UDP/SCTP",
    udp_portrange="53",
)
ping = ServiceCustom(name="example-ping", protocol="ICMP", icmptype=8, icmpcode=0)
fmg.add([web, dns, ping])
```

## PortRange

`PortRange` is a local helper for service port fields. It is serialized through `ServiceCustom`;
do not pass it to `fmg.add()`. Strings use destination ports first, followed by optional source
ports after a colon: `destination-start-destination-end:source-start-source-end`.

```python
from pyfortinet.fmg_api.firewall import PortRange, ServiceCustom

restricted = ServiceCustom(
    name="example-restricted-web",
    tcp_portrange=[
        "443",
        PortRange(
            destination_start="8443", destination_end="8444",
            source_start="1024", source_end="65535",
        ),
    ],
)
assert restricted.model_dump(by_alias=True, exclude_none=True)["tcp-portrange"] == [
    "443", "8443-8444:1024-65535"
]
fmg.add(restricted)
```

A single port accepts either endpoint: `PortRange(destination_end="443")` serializes to `443`
when used in a service. Start values greater than end values raise a validation error.
String and model entries may be mixed in either order; invalid entries are rejected.

## ServiceGroup

Create services before the group. Like address groups, service groups accept names or named
models as members. This example uses the custom services created above:

```python
from pyfortinet.fmg_api.firewall import ServiceGroup

services = ServiceGroup(name="example-application-services", member=[web, dns, "example-ping"])
fmg.add(services)
```
