# Device operations

The `dvmcmd` module represents device-manager execution operations. Use these for managed-device
lifecycle workflows, rather than assuming `Device.add()` or `Device.delete()` has equivalent
semantics. Read the [device inventory guide](dvmdb.md) and [task guide](tasks.md) first.

## DeviceCommand

`DeviceCommand` extends the inventory model with command-specific fields, including
`device_action` and `device_blueprint`. Constructing it makes no request:

```python
from pyfortinet.fmg_api.dvmcmd import DeviceCommand

candidate = DeviceCommand(
    name="example-model-fw",
    sn="FGVMEXAMPLE000001",
    device_action="add_model",
)
```

This is an illustrative model-device definition. Replace the serial number and supply any
additional platform or version fields required by your target firmware before execution.
This documentation update does not establish a complete enrollment recipe for every firmware.

## DeviceTask

A `DeviceTask` takes an explicit ADOM and a `Device` or `DeviceCommand` instance.
The action selects the add or delete command. Build an add request locally:

```python
from pyfortinet.fmg_api.dvmcmd import DeviceTask

add_task = DeviceTask(
    adom=fmg.adom,
    device=candidate,
    action="add",
    flags=["create_task"],
)
```

Only execute the request after checking the target, prerequisites, and unused device identity:

```python
response = fmg.exec(add_task)
state = response.wait_for_task()
if state != "done":
    raise RuntimeError(f"Device operation did not complete successfully: {state}")
```

Keep the connection open while polling. The response can indicate request acceptance before the
device-manager operation completes.

For removal, construct a separate request using an explicitly named existing device:

```python
from pyfortinet.fmg_api.dvmdb import Device

remove_task = DeviceTask(
    adom=fmg.adom,
    device=Device(name="retired-example-fw"),
    action="del",
    flags=["create_task"],
)
```

This snippet only constructs the removal request. Executing it removes the device from
FortiManager and can have consequences beyond object cleanup. The current constructor expects
a device model even for deletion; it converts that model to its name in the request payload.
Workspace discard does not provide a general undo for device lifecycle operations.
