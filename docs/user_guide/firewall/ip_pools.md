# IP pools

Use an open connection from the [quickstart](../quickstart.md). Run the snippets on this page in order;
write examples require unused names and valid references in your selected ADOM. Await requests
when using an asynchronous client. See the [firewall overview](../firewall_objects.md) for
firmware coverage and shared conventions.

## IPPool

`IPPool` uses `firewall/ippool`. It supports the reference's overload, one-to-one,
fixed-port-range, port-block-allocation, and CGN resource-allocation types. IP values and metadata
variables remain strings; array inputs such as `exclude_ip` preserve the API's list shape.

## IPPoolDynamicMapping

Use `IPPoolDynamicMapping` for mapping-specific fields, including IPv6 source prefixes, client
prefix length, session quotas, and privileged-port PBA settings. Scope and mapping-array handling
match `VIPDynamicMapping`; mapping-only fields are not sent on the parent object.

```python
from pyfortinet.fmg_api.common import Scope
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

## IPPoolGroup

`IPPoolGroup` uses the schema's `firewall/ippool_grp` route, with an underscore. Members can be
pool names or `IPPool` objects and serialize as names. Member pools must use
`type="cgn-resource-allocation"`, have the same attributes except their public/client ranges,
and belong to only one pool group. FMG enforces these relationships; the CGN type and exclusive
membership requirements were verified on FMG 7.4.6 build 2588.
Cloning a populated group attempts to reuse its pools and is rejected by that firmware.
The group itself has no dynamic mapping in this reference; mappings belong to its member pools.

```python
from pyfortinet.fmg_api.firewall import IPPool, IPPoolGroup

pool = IPPool(
    name="cgn-pool", type="cgn-resource-allocation", startip="203.0.113.10", endip="203.0.113.19",
)
fmg.add(pool)
group = IPPoolGroup(name="outbound-pools", member=[pool])
fmg.add(group)
```
