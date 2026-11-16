# Proxy objects

Use an open connection from the [quickstart](../quickstart.md). Run the snippets on this page in order;
write examples require unused names and valid references in your selected ADOM. Await requests
when using an asynchronous client. See the [firewall overview](../firewall_objects.md) for
firmware coverage and shared conventions.

## ProxyAddress

The `example-server` address referenced below must already exist.

`ProxyAddress` uses `firewall/proxy-address` in the selected ADOM or global scope. It supports
header-group and tagging rows, HTTP method/browser arrays, and named host-address references.
Single array values are accepted and serialized as arrays; references can be names or named
high-level objects. `_image-base64` is exposed as `image_base64` in Python.

```python
from pyfortinet.fmg_api.firewall import Address, ProxyAddress

address = ProxyAddress(
    name="example-proxy-site", type="host-regex", host_regex=r".*\.example\.com",
    host=Address(name="example-server"), case_sensitivity="disable",
)
fmg.add(address)
```

The reference defines no proxy-address dynamic mapping; none is added by this client.

## ProxyAddressGroup

`ProxyAddressGroup` uses `firewall/proxy-addrgrp`. Members can be names or named objects and
serialize as name arrays. `type` accepts `src` or `dst`. An omitted member field leaves it out
of a write; `member=[]` explicitly sends an empty array. Tagging rows are supported.

```python
from pyfortinet.fmg_api.firewall import ProxyAddressGroup

group = ProxyAddressGroup(name="example-sites", type="dst", member=[address])
fmg.add(group)
```

The reference defines no proxy-address-group dynamic mapping.


## ProxyAddressHeaderGroup

These helper models are embedded in a `ProxyAddress`. Header rows express HTTP header matching;
tagging rows refer to existing categories and tags. Unlike `AddressTagging`, proxy tagging
categories use lists.

```python
from pyfortinet.fmg_api.firewall import (
    ProxyAddress,
    ProxyAddressHeaderGroup,
    ProxyAddressTagging,
)

header_address = ProxyAddress(
    name="example-header",
    type="header",
    header_group=[
        ProxyAddressHeaderGroup(
            id=1, header_name="X-Environment", header="production", case_sensitivity="disable"
        )
    ],
    tagging=[
        ProxyAddressTagging(name="business-role", category=["Role"], tags=["Backend"])
    ],
)
fmg.add(header_address)
```

## ProxyAddressTagging

`ProxyAddressTagging` adds category and tag references to a proxy address. The preceding example
embeds it in the initial ADD. To replace the tags on an existing proxy address, use a partial update:

```python
from pyfortinet.fmg_api.firewall import ProxyAddress, ProxyAddressTagging

fmg.update(ProxyAddress(
    name="example-header",
    tagging=[ProxyAddressTagging(name="business-role", category=["Role"], tags=["Frontend"])],
))
```

This sends the complete replacement tagging list. The category and tags must already be available.

## ProxyAddressGroupTagging

Use `ProxyAddressGroupTagging` for metadata embedded in a proxy group. Member proxy addresses,
categories, and tags must already exist:

```python
from pyfortinet.fmg_api.firewall import ProxyAddressGroup, ProxyAddressGroupTagging

tagged_group = ProxyAddressGroup(
    name="example-tagged-sites",
    type="dst",
    member=["example-proxy-site"],
    tagging=[
        ProxyAddressGroupTagging(name="business-role", category=["Role"], tags=["Backend"])
    ],
)
fmg.add(tagged_group)
```
