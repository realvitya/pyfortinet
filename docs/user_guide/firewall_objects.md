# Additional firewall objects

These classes are imported from `pyfortinet.fmg_api.firewall` and work with both `FMG` and
`AsyncFMG`. Their fields follow the supplied **FortiManager 7.6.7 Configuration Database v7.4
ADOM Level Objects** schema. Fields are optional for collection queries, partial GET responses,
and partial updates. Only supplied values are written when absent values are excluded by the client.
Python field names use underscores; outgoing payloads use the documented API aliases.

Verification uses the supplied schema and mocked transport. Live compatibility with FMG 7.6.7
has not been verified. No configuration is installed by constructing these objects.

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
