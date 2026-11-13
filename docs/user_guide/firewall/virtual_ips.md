# Virtual IPs

Use an open connection from the [quickstart](../quickstart.md). Run the snippets on this page in order;
write examples require unused names and valid references in your selected ADOM. Await requests
when using an asynchronous client. See the [firewall overview](../firewall_objects.md) for
firmware coverage and shared conventions.

## VIP

`VIP` uses `firewall/vip`, with complete fields for static NAT, load balancing, SSL, real servers,
GSLB, and QUIC from the reference. Array fields accept one value or a list. Address ranges and
metadata-variable strings are preserved without imposing IP-only validation.

## VIPDynamicMapping

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
