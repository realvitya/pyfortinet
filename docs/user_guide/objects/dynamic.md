# Normalized interfaces

Normalized interfaces let policy configuration refer to a logical interface name rather than
one physical interface on every device. The `dynamic` module models the parent and its mappings.
Use an open connection as described in the [object guide](index.md).

## NormalizedInterface

Read existing definitions or create a new definition with a default interface mapping:

```python
from pyfortinet.fmg_api.dynamic import NormalizedInterface

interfaces = fmg.get(NormalizedInterface).data
for interface in interfaces:
    print(interface.name, interface.defmap_intf)

normalized = NormalizedInterface(
    name="example-lan",
    default_mapping="enable",
    defmap_intf="port1",
)
fmg.add(normalized)
```

The new name must be unused and the default mapping must be appropriate for the target devices.
This creates FortiManager object configuration; it does not install a device interface.

## DynamicMapping

`DynamicMapping` describes device/VDOM overrides nested in a normalized interface. Inspect
returned entries through their parent:

```python
parent = fmg.get(NormalizedInterface(name="example-lan")).first()
if parent is not None:
    mappings = parent.dynamic_mapping or []
    if not isinstance(mappings, list):
        mappings = [mappings]
    for mapping in mappings:
        print(mapping.mapping__scope, mapping.local_intf)
```

To construct an override locally:

```python
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.dynamic import DynamicMapping

override = DynamicMapping(
    mapping__scope=Scope(name="branch-fw", vdom="root"),
    local_intf=["port2"],
)
draft = NormalizedInterface(name="example-lan", dynamic_mapping=[override])
payload = draft.model_dump(by_alias=True, exclude_none=True)
assert payload["dynamic_mapping"][0]["local-intf"] == ["port2"]
```

## PlatformMapping

`PlatformMapping` describes a platform-specific interface mapping. Construct or inspect it as
nested parent data:

```python
from pyfortinet.fmg_api.dynamic import PlatformMapping

platform = PlatformMapping(name="FortiGate-VM64", intf_zone="port1")
draft = NormalizedInterface(name="example-platform-lan", platform_mapping=[platform])
payload = draft.model_dump(by_alias=True, exclude_none=True)
assert payload["platform_mapping"][0]["intf-zone"] == "port1"
```

Replace the platform identifier with one supported by your FortiManager. These mapping examples
demonstrate local model construction and serialization, not verified mapping writes.

Both mapping classes retain legacy `get_url` property overrides that are incompatible with the
clients' current `get_url(method=...)` calling convention. Standalone mapping CRUD is therefore
not presented as a supported workflow. The parent `NormalizedInterface` supports normal object
requests; confirm firmware behavior before submitting nested mapping changes.
