# Advanced usage / extension of the handler

It is possible to extend the FMG handler capabilities with custom methods. If the existing methods are not enough or
seem too atomic, custom methods and behaviour can be attached to the handler.

Here is an example why and how it can be done:

## Adding human-readable actions

Let's say we want to add more complex tasks as method to the handler itself so our code can be clean and focused on its
task.

```python title="mypkg/mymodule/myfmg.py"
from pyfortinet import FMG
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.dvmcmd import DeviceTask
from pyfortinet.fmg_api.policy import PolicyPackage, PackageSettings, Policy


class MyFMG(FMG):
    """Extra actions for FortiManager"""
    def create_firewall(self, name: str, address: str, serial: str) -> bool:
        """This method creates a device along with a default firewall policy

        Firewall will be deleted if existed before!

        Notes:
            This method may leave garbage after itself if exception is raised anywhere!

        Arguments:
            name (str): The name of the device
            address (str): The IP address of the device
            serial (str): The serial number of the device

        Returns:
            (bool): True if the device was created successfully, False otherwise
        """
        # sanity check
        name = name.strip().upper()
        try:
            # create device
            device: Device = Device(name=name, sn=serial, os_ver="7.0", mr=2, ip=address)
            if existing_device:=self.get(device).first():
                delete_job = DeviceTask(adom=self.adom, device=existing_device, action="del")
                self.exec(delete_job)
            job = DeviceTask(adom=self.adom, device=device)
            result = self.exec(job)
            status = result.wait_for_task()
            if status != "done":
                return False
            fw: Device = self.get(Device(name=name)).first()
            # create PolicyPackage
            pp_settings = PackageSettings(fwpolicy_implicit_log="enable")
            pp = self.get_obj(PolicyPackage, name=name, scope_member=[fw.get_vdom_scope("root")], package_settings=pp_settings)
            pp.add()
            pp.refresh()
            default_policies = [
                Policy(pkg=pp.name, name="Default explicit deny 1->2", srcaddr=["all"], dstaddr=["all"], srcintf=["port1"],
                       dstintf=["port2"], action="deny", service=["ALL"], logtraffic="disable", schedule=["always"]),
                Policy(pkg=pp.name, name="Default explicit deny 2->1", srcaddr=["all"], dstaddr=["all"], srcintf=["port2"],
                       dstintf=["port1"], action="deny", service=["ALL"], logtraffic="disable", schedule=["always"])
            ]
            self.add(default_policies)
            return True
        except Exception:
            return False
```

Then your code is cleaner by simply calling the modified handler with custom method:

```python title="mypkg/mymodule/app.py"
from mymodule.myfmg import MyFMG
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conn_data = {
    "base_url": "https://fmg",
    "verify": False,
    "username": "admin",
    "password": "verysecret",
    "adom": "root"
}

with MyFMG(**conn_data) as fmg:
    fmg.create_firewall("mytestfw", "1.1.1.1", "FG100FTK22345678")
```

## Explicit workspace locking

Use `with fmg.lock_adom("root"):` for synchronous operations and
`async with fmg.lock_adom("root"):` for asynchronous operations. The context releases locks it acquired,
including when the operation raises an exception. Existing locks are preserved; `keep_locked=True` also
preserves a newly acquired lock. Unlocking a selected ADOM leaves other ADOM locks intact.
`lock_adoms()` and `unlock_adoms()` return successful responses only when all requested operations
succeed, and their data includes a result for each ADOM. Workspace mode discovery raises
`FMGLockException` when its reply is unsuccessful or incomplete and leaves the cached mode unset.

## Selecting fields and scopes

High-level `get` calls accept `fields=["name", ...]` to request selected fields. Returned objects retain
the scope used by the request, so their later operations continue to target that scope even when the
client's selected ADOM changes. An object's explicit scope takes precedence over the request's scope.
Successful high-level GET replies with absent or null data return an empty object list.

## Waiting for tasks

Both clients accept task responses containing either `taskid` or `task` and retry transient connection
failures until the polling timeout. Async callbacks may be functions or callable objects returning an awaitable.

## Connection cleanup

Malformed login replies and missing session tokens raise `FMGTokenException` in both clients.

Calling `open()` on an already open client keeps the existing session and workspace locks. To start
a new session, close the client first.

`close()` is safe before opening a connection and after it has already been closed. Both clients release
the HTTP session and clear authentication and cached workspace state even if logout fails. For async
clients, await `close()`.

`close(discard_changes=True)` applies only to that close operation. It leaves the configured
`discard_on_close` setting unchanged when the client is opened again.

## Batch write validation

Write batches must be nonempty and contain either only request dictionaries or only API objects.
Low-level clients accept dictionaries only. Invalid batches raise `FMGWrongRequestException`, or return
a failed response when `raise_on_error=False`, before contacting FortiManager.

## Invalid API replies

Malformed JSON-RPC replies, including empty result lists and missing status codes, raise
`FMGUnhandledException`. With `raise_on_error=False`, calls return a failed response instead. Successful
GET results may still contain absent or null data; the result envelope must include a valid status code.

## Combining filters

Filter combinations preserve nested expressions when using `&`, `|`, and `+`. Only adjacent filter
lists with the same operator are flattened, so explicit grouping is retained.

## Custom service port ranges

For a single port, `PortRange` accepts either the start or end endpoint. For example,
`PortRange(destination_start="443")` and `PortRange(destination_end="443")` both serialize to `443`.

Service port-range lists can mix strings and `PortRange` objects in either order. Invalid entries raise
a Pydantic `ValidationError` instead of being silently omitted. Explicit `None` values remain unset.

## Optional collection serialization

Optional member, category, and port-range collections preserve `None` during model serialization.
Explicit empty lists remain empty lists, allowing them to clear an existing collection.

## Response lookup

A low-level response containing one dictionary supports `response[0]` and
`response["object-name", "name"]`, like a response containing a list of result dictionaries.
For API objects without declared master keys, supply the lookup field explicitly.
