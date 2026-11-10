# Devices and ADOMs

The `dvmdb` module models FortiManager's device inventory and administrative domains.
Use the connection and scope conventions in the [object guide](index.md).

## ADOM

Read the ADOM inventory or select an ADOM by name:

```python
from pyfortinet.fmg_api.dvmdb import ADOM

adoms = fmg.get(ADOM).data
for adom in adoms:
    print(adom.name, adom.desc)

selected = fmg.get(ADOM(name="branch-adom")).first()
if selected is not None:
    print(selected.name, selected.workspace_mode)
```

ADOM inventory uses a system-wide route. Selecting `fmg.adom` does not restrict this inventory
to that one ADOM; permissions still apply.

To change the description of an existing ADOM, target it explicitly:

```python
fmg.update(ADOM(name="branch-adom", desc="Branch administration"))
```

ADOM creation, deletion, and cloning affect lifecycle state. The model exposes the corresponding
object operations, but confirm the target and firmware requirements before using them. They are
not made safe by choosing another ADOM in the connection settings.

## Device

`Device` describes a managed device in the selected ADOM. Use filters to choose a device,
rather than taking the first device in an inventory:

```python
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device

connected = fmg.get(Device, F(conn_status="up")).data
device = fmg.get(Device(name="branch-fw")).first()
if device is not None:
    print(device.name, device.hostname, device.conf_status)
```

To change inventory metadata for that existing device:

```python
fmg.update(Device(name="branch-fw", desc="Branch edge firewall"))
```

For adding or removing a managed device, use the command objects in
[device operations](device_operations.md). Do not assume generic configuration CRUD performs
the same lifecycle workflow.

## VDOM

A `VDOM` lookup needs its parent device as well as the selected ADOM:

```python
from pyfortinet.fmg_api.dvmdb import VDOM

vdoms = fmg.get(VDOM(device="branch-fw")).data
root_vdom = fmg.get(VDOM(device="branch-fw", name="root")).first()
for vdom in vdoms:
    print(vdom.name, vdom.comments)
```

`device` locates the parent and is excluded from the configuration payload.
To obtain a mapping scope from an inventory record with loaded VDOMs:

```python
device = fmg.get(Device(name="branch-fw")).first()
if device is not None and device.vdom:
    scope = device.get_vdom_scope("root")
    if scope is not None:
        print(scope.name, scope.vdom)
```

`get_vdom_scope()` uses the loaded `device.vdom` list; it does not fetch missing VDOM data.
Handle absent VDOM data and a nonmatching VDOM explicitly.

## HASlave

`HASlave` represents nested HA member records returned in `Device.ha_slave`. It has no
independent endpoint in the implementation. Inspect it through a device response:

```python
device = fmg.get(Device(name="branch-fw")).first()
if device is not None:
    for member in device.ha_slave or []:
        print(member.name, member.role, member.status, member.conf_status)
```

A standalone `fmg.get(HASlave)` or write is not a supported workflow. Despite the historical
class name, each record includes a `role` field that identifies its HA role.
