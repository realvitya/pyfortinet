# Device system settings

The `system` models address configuration stored in FortiManager for a managed FortiGate.
They use explicit device names rather than a direct connection to the FortiGate.
See the [object guide](index.md) for connection conventions.

## DeviceInterface

Read interfaces for an explicitly named device:

```python
from pyfortinet.fmg_api.system import DeviceInterface

interfaces = fmg.get(DeviceInterface(device="branch-fw")).data
port = fmg.get(DeviceInterface(device="branch-fw", name="port1")).first()
for interface in interfaces:
    print(interface.name, interface.alias)
```

To update an existing interface alias in FortiManager's database:

```python
fmg.update(DeviceInterface(device="branch-fw", name="port1", alias="Branch LAN"))
```

`name` identifies the interface. `interface` is a separate parent-interface reference, used
for VLANs and similar relationships. `device` and `fmg_interface` are URL-only fields.
A local VLAN definition illustrates that distinction:

```python
vlan = DeviceInterface(
    device="branch-fw",
    name="example-vlan",
    type="vlan",
    interface="port1",
    vlanid=123,
    vdom="root",
    ip="192.0.2.1/24",
)
```

This definition is not submitted. Device/platform support and interface dependencies must be
checked before adding it. See [advanced usage](../advanced_usage.md#device_system_configuration_schemas)
for the schema source and compatibility limits.

## DeviceZone

Zones belong to a device and VDOM. Read the zone collection:

```python
from pyfortinet.fmg_api.system import DeviceZone

zones = fmg.get(DeviceZone(device="branch-fw", vdom="root")).data
for zone in zones:
    print(zone.name, zone.interface)
```

To create a new zone using existing interfaces:

```python
zone = DeviceZone(
    device="branch-fw",
    vdom="root",
    name="example-zone",
    interface=["port2"],
    intrazone="deny",
)
fmg.add(zone)
```

Use an unused zone name and an interface eligible for membership in that VDOM. Interface model
references are also accepted and converted to names. The parent device and VDOM are excluded
from the configuration payload.

## SystemAdmin

`SystemAdmin` addresses administrator configuration on the managed device, not FortiManager's
own administrator accounts. It can return sensitive configuration; print only the fields needed.

```python
from pyfortinet.fmg_api.system import SystemAdmin

admins = fmg.get(SystemAdmin(device="branch-fw")).data
for admin in admins:
    print(admin.name)
```

To update a comment on an explicitly selected existing account:

```python
fmg.update(SystemAdmin(
    device="branch-fw",
    name="existing-automation-user",
    comments="Managed by the automation team",
))
```

Changes remain in FortiManager's device configuration database until an appropriate installation.
Review pending device settings before installing; installation may include unrelated pending changes.
