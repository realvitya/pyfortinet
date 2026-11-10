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
