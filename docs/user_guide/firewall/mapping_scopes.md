# Mapping scopes

Use an open connection from the [quickstart](../quickstart.md). Run the snippets on this page in order;
write examples require unused names and valid references in your selected ADOM. Await requests
when using an asynchronous client. See the [firewall overview](../firewall_objects.md) for
firmware coverage and shared conventions.

## Scope

`Scope` identifies a managed device and, where applicable, its VDOM. It is shared by several API
domains and re-exported by the firewall package for convenience. It is not a resource to add.

```python
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.firewall import Address

device_scope = Scope(name="branch-fw", vdom="root")
mapping = Address(mapping__scope=device_scope, subnet="198.51.100.10/32")
override = Address(name="example-server", dynamic_mapping=[mapping])
fmg.update(override)
```

The device, VDOM, and parent address must already exist. This replaces the address's entire
mapping list with the supplied override; preserve other entries if they must remain.
