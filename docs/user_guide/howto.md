# How-tos

These examples use the imports and `config` from the [quickstart](quickstart.md).
Unless a connection context is shown, run the snippet inside `with FMG(**config) as fmg:`.
Replace example names with resources in your selected ADOM. Write examples modify FortiManager;
installation examples also modify the selected FortiGate.

## Find and filter objects

```python
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.firewall import Address

servers = fmg.get(Address, F(name__like="server%"), fields=["name", "subnet"]).data
offline = fmg.get(Device, F(name__like="branch-%") & ~F(conn_status="up")).data
either = fmg.get(Address, F(name="server1") | F(name="server2")).data
```

Use parentheses to make grouping explicit. `&` combines conditions with AND, `|` with OR,
and `~` negates a condition. `+` creates the API's implicit OR list.
An initialized model can also select an object: `fmg.get(Address(name="server1")).first()`.
Always handle `None` before accessing the result of `.first()`.

## Create and bind objects

```python
address = Address(name="example-server", subnet="192.0.2.10/32")
fmg.add(address)

bound = fmg.get_obj(Address, name="example-backend", subnet="192.0.2.20/32")
bound.add()
```

Constructing or binding a model does not contact FortiManager. Both `fmg.add(address)` and
`bound.add()` submit an ADD request. Use names that do not already exist.

## Update, refresh, and delete

```python
server = fmg.get(Address(name="example-server")).first()
if server is None:
    raise LookupError("example-server does not exist")

fmg.update(Address(name=server.name, comment="Managed by the application"))
server.refresh()
print(server.comment)
```

To delete that address after removing any references to it:

```python
server.delete()
```

`refresh()` reloads a bound object in place and requires exactly one match. `update()` sends
the model's non-null fields; using a small model limits the fields sent. `None` is omitted
from high-level write payloads. An explicit empty list is sent and can clear a collection.

## Create an address group

Create member addresses before the group that references them:

```python
from pyfortinet.fmg_api.firewall import AddressGroup

backend = Address(name="example-group-backend", subnet="192.0.2.30/32")
fmg.add(backend)
group = AddressGroup(name="example-backends", member=[backend])
fmg.add(group)
```

Members may be object instances or names; the serializer sends their names. Supplying a member
object does not create it automatically. When removing these resources, delete the group first.

## Add or remove a device-specific address mapping

The address and device must already exist. Select the device explicitly:

```python
server = fmg.get(Address(name="example-server")).first()
device = fmg.get(Device(name="branch-fw")).first()
if server is None or device is None:
    raise LookupError("The example address and branch-fw device must already exist")

mapping = Address(
    mapping__scope=device.get_vdom_scope("root"),
    subnet="198.51.100.10/32",
)
# This example replaces the complete mapping collection with one override.
fmg.update(Address(name=server.name, dynamic_mapping=[mapping]))
server.refresh()
print(server.dynamic_mapping)
```

Use the target device's actual VDOM. Preserve existing mapping entries if they must remain.
To remove all overrides from this address:

```python
fmg.update(Address(name=server.name, dynamic_mapping=[]))
server.refresh()
```

Mappings are embedded in the address payload. A GET returns a response; use `.first()` to
obtain the address before accessing its attributes.

## Work with workspace locks

Automatic locking handles lock-required API replies. To hold a lock across a known operation:

```python
with FMG(**config) as fmg:
    with fmg.lock_adom(fmg.adom):
        fmg.update(Address(name="example-server", comment="Reviewed configuration"))
        fmg.lock.commit_changes([fmg.adom])
```

Commit before leaving an explicit lock context when changes should be saved. The context releases
a lock it acquired; it preserves an existing lock or a lock requested with `keep_locked=True`.
Normal connection cleanup attempts to commit locks still held by the client. Set
`discard_on_close=True` to skip that commit. Workspace settings apply only where workspace
is enabled and do not undo installations or provide a transaction across all operations.

For async clients, use `async with fmg.lock_adom(...)` and await requests and
`fmg.lock.commit_changes(...)`. Workflow session creation and approval are not automated.
See [advanced usage](advanced_usage.md#explicit_workspace_locking) for scope rules.

## Install device settings and wait for completion

This operation installs device settings onto the explicitly named FortiGate. Review pending
configuration first; installation can include changes made outside this script.
Use an existing device and VDOM in the selected ADOM.

```python
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.securityconsole import InstallDeviceTask

with FMG(**config) as fmg:
    task = fmg.get_obj(
        InstallDeviceTask,
        adom=fmg.adom,
        scope=[Scope(name="branch-fw", vdom="root")],
        flags=["auto_lock_ws"],
    )
    response = task.exec()
    state = response.wait_for_task(
        callback=lambda percent, log: print(f"Task at {percent}%: {log}")
    )
    if state != "done":
        raise RuntimeError(f"Installation did not complete successfully: {state}")
```

Keep the connection open while waiting. A successful execution response means the request was
accepted; check the task state separately. Not every execution response contains a task ID.
`wait_for_task()` returns `None` when there is no task to poll or a task-status request fails.

For an async client, use `response = await task.exec()` and
`state = await response.wait_for_task()`.

## Handle request failures

By default, library API failures raise exceptions. Handle the specific exception appropriate to
your workflow, or catch `FMGException` at an application boundary:

```python
from pyfortinet.exceptions import FMGException

try:
    with FMG(**config) as fmg:
        addresses = fmg.get(Address).data
except FMGException:
    print("The FortiManager request failed")
```

With `raise_on_error=False`, decorated JSON-RPC operations return failed responses for library
exceptions; check `response.success` before using data. This setting does not suppress every
Python, validation, transport, or refresh error. See
[advanced usage](advanced_usage.md#transport_retries_and_timeouts) for transport exceptions.
