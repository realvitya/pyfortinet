# Additional firewall objects

These classes are imported from `pyfortinet.fmg_api.firewall` and work with both `FMG` and
`AsyncFMG`. Their fields follow the supplied **FortiManager 7.6.7 Configuration Database v7.4
ADOM Level Objects** schema. Fields are optional for collection queries, partial GET responses,
and partial updates. Only supplied values are written when absent values are excluded by the client.
Python field names use underscores; outgoing payloads use the documented API aliases.

Verification uses the supplied schema and mocked transport. Live compatibility with FMG 7.6.7
has not been verified. No configuration is installed by constructing these objects.
Live scenarios passed on FMG 7.4.6 build 2588 for the five writable object types and the VIP/IPPool
mappings. InternetService live lookups were skipped because that lab's catalog was empty.
Sync and async lab scenarios are available in the
[testing guide](../developer_guide/testing.md#additional_firewall_lab_scenarios).

## Proxy addresses

`ProxyAddress` uses `firewall/proxy-address` in the selected ADOM or global scope. It supports
header-group and tagging rows, HTTP method/browser arrays, and named host-address references.
Single array values are accepted and serialized as arrays; references can be names or named
high-level objects. `_image-base64` is exposed as `image_base64` in Python.

```python
from pyfortinet.fmg_api.firewall import Address, ProxyAddress

address = ProxyAddress(
    name="example-site", type="host-regex", host_regex=r".*\.example\.com",
    host=Address(name="backend"), case_sensitivity="disable",
)
fmg.add(address)
```

The reference defines no proxy-address dynamic mapping; none is added by this client.

## Proxy address groups

`ProxyAddressGroup` uses `firewall/proxy-addrgrp`. Members can be names or named objects and
serialize as name arrays. `type` accepts `src` or `dst`. An omitted member field leaves it out
of a write; `member=[]` explicitly sends an empty array. Tagging rows are supported.

```python
from pyfortinet.fmg_api.firewall import ProxyAddressGroup

group = ProxyAddressGroup(name="example-sites", type="dst", member=[address])
fmg.add(group)
```

The reference defines no proxy-address-group dynamic mapping.

## Internet services

`InternetService` models the Internet Service Database fields on `firewall/internet-service`.
The supplied reference exposes only GET, SET, and UPDATE at the collection URL. It defines no
ADD, DELETE, CLONE, item-by-ID URL, or dynamic mapping. Unsupported object operations raise
`FMGWrongRequestException` before sending a request.

```python
from pyfortinet.fmg_api.firewall import InternetService

service = fmg.get(InternetService(id=65536)).first()  # id becomes a GET filter
```

An ID remains in SET/UPDATE data; it is not appended to the URL. Firmware decides which
database attributes are editable; the reference does not mark individual fields read-only.

## Virtual IPs

`VIP` uses `firewall/vip`, with complete fields for static NAT, load balancing, SSL, real servers,
GSLB, and QUIC from the reference. Array fields accept one value or a list. Address ranges and
metadata-variable strings are preserved without imposing IP-only validation.

`VIPDynamicMapping` is a separate model because the mapping schema has different fields and
types: for example, parent `extintf` is an array, mapping `extintf` is a string, and mapping real
servers include `seq`. Pass a mapping object/dictionary or a list in `dynamic_mapping`; it is
always serialized as an array. `mapping__scope` accepts a `Scope`, dictionary, or list and uses
the API alias `_scope` on the wire.

```python
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.firewall import VIP, VIPDynamicMapping

vip = VIP(
    name="web", extintf="wan1", extip="203.0.113.10", mappedip="192.0.2.10",
    portforward="enable", extport="443", mappedport="8443",
    dynamic_mapping=VIPDynamicMapping(
        mapping__scope=Scope(name="FG01", vdom="root"),
        extintf="wan2", extip="203.0.113.20", mappedip="192.0.2.20",
    ),
)
fmg.add(vip)
```

Mappings are embedded in parent writes, as with existing address mappings. GET returns typed
mapping rows. Use `dynamic_mapping=[]` in an update to send an empty mapping array; leaving it
`None` omits the field. Separate mapping-endpoint CRUD wrappers are not provided.

## IP pools

`IPPool` uses `firewall/ippool`. It supports the reference's overload, one-to-one,
fixed-port-range, port-block-allocation, and CGN resource-allocation types. IP values and metadata
variables remain strings; array inputs such as `exclude_ip` preserve the API's list shape.

Use `IPPoolDynamicMapping` for mapping-specific fields, including IPv6 source prefixes, client
prefix length, session quotas, and privileged-port PBA settings. Scope and mapping-array handling
match `VIPDynamicMapping`; mapping-only fields are not sent on the parent object.

```python
from pyfortinet.fmg_api.firewall import IPPool, IPPoolDynamicMapping

pool = IPPool(
    name="outbound", type="overload", startip="203.0.113.10", endip="203.0.113.19",
    dynamic_mapping=IPPoolDynamicMapping(
        mapping__scope=Scope(name="FG01", vdom="root"),
        startip="203.0.113.20", endip="203.0.113.29",
    ),
)
fmg.add(pool)
```

## IP pool groups

`IPPoolGroup` uses the schema's `firewall/ippool_grp` route, with an underscore. Members can be
pool names or `IPPool` objects and serialize as names. Member pools must use
`type="cgn-resource-allocation"`, have the same attributes except their public/client ranges,
and belong to only one pool group. FMG enforces these relationships; the CGN type and exclusive
membership requirements were verified on FMG 7.4.6 build 2588.
Cloning a populated group attempts to reuse its pools and is rejected by that firmware.
The group itself has no dynamic mapping in this reference; mappings belong to its member pools.

```python
from pyfortinet.fmg_api.firewall import IPPoolGroup

pool = IPPool(
    name="cgn-pool", type="cgn-resource-allocation", startip="203.0.113.10", endip="203.0.113.19",
)
fmg.add(pool)
group = IPPoolGroup(name="outbound-pools", member=[pool])
fmg.add(group)
```
