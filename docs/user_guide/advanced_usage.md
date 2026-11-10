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

## Choosing sync or async context management

`FMG` supports both connection context protocols:

```python
with FMG(**settings) as fmg:
    addresses = fmg.get(Address).data

async def read_addresses():
    async with FMG(**settings) as fmg:
        return (await fmg.get(Address)).data
```

Each async entry creates a separate `AsyncFMG` client with async methods and response types. Objects fetched
or bound with `fmg.get_obj(...)` inside that context use this async client as well. Use the value bound
by `as fmg` for operations; the original manager retains its synchronous API.

A manager can be reused sequentially in either mode. Its configuration is shared with the yielded
async client, so changes to properties such as `adom` and `raise_on_error` persist between contexts.
Overlapping async contexts or mixing an open sync connection with an async context on the same manager
raise `FMGConfigurationException`. Separate managers can be used independently.

`FMG.open()` and `FMG.close()` remain synchronous. Use `AsyncFMG` for manual `await client.open()` and
`await client.close()` management. Async context cleanup preserves the existing discard-on-error
behavior and propagates exceptions. Custom synchronous subclass methods are not converted to async methods.

## Explicit workspace locking

Use `with fmg.lock_adom("root"):` for synchronous operations and
`async with fmg.lock_adom("root"):` for asynchronous operations. The context releases locks it acquired,
including when the operation raises an exception. Existing locks are preserved; `keep_locked=True` also
preserves a newly acquired lock. Unlocking a selected ADOM leaves other ADOM locks intact.
`lock_adoms()` and `unlock_adoms()` return successful responses only when all requested operations
succeed, and their data includes a result for each ADOM. Workspace mode discovery raises
`FMGLockException` when its reply is unsuccessful or incomplete and leaves the cached mode unset.

Discovery uses the global workspace setting unless it is `per-adom`. In that case it reads
`workspace_mode` from `/dvmdb/adom/{adom}` for the requested ADOM. Each explicit locking context
refreshes discovery, so switching ADOMs cannot reuse another ADOM's setting. Calling `fmg.lock()`
without arguments uses the selected ADOM (or `root` when none is selected); with multiple ADOMs,
only those with workspace enabled are locked. Normal and workflow modes both require locking;
this does not create workflow sessions. Closing the client still cleans up retained locks even
if the last ADOM checked has workspace disabled.

The Global Database does not use a workspace when global mode is `per-adom`, so automatic
locking skips `global` in that mode. Under global `normal` and `workflow`, it requires locking.
This behavior was verified on FMG 7.4.6 build 2588 by temporarily changing global mode and the
`test` ADOM's workspace setting through all 12 combinations, reading both levels, and probing
Global Database locks. All settings were restored, acquired locks released, and sessions logged out;
no policy/object changes, configuration installs, or workspace commits were performed.

| Global `workspace-mode` | Requested ADOM `workspace_mode` | Returned ADOM `workspace_mode` | Global lock result |
|-------------------------|---------------------------------|--------------------------------|--------------------|
| `disabled`              | 0, 1, or 2                      | 0                              | -9 (unavailable)   |
| `normal`                | 0, 1, or 2                      | 1                              | 0 (success)        |
| `workflow`              | 0, 1, or 2                      | 2                              | 0 (success)        |
| `per-adom`              | 0, 1, or 2                      | Requested value                | -9 (unavailable)   |

The ADOM metadata reports the effective mode, including global overrides. A lock-info record's
`db_mode` is not a substitute: it reported 1 for a locked ADOM even under global `workflow`.
Neither `/dvmdb/adom/global` nor `/dvmdb/adom/Global` returned metadata (status `-3`), and the
ADOM inventory contained no Global Database entry. GET `/dvmdb/global/workspace/lockinfo`
returned `-9` under `disabled` and `per-adom`, and succeeded under `normal` and `workflow`.
The explicit Global Database rule comes from these controlled checks, not from treating arbitrary
failed metadata reads as disabled workspace. Failed ordinary ADOM discovery still raises
`FMGLockException`. Other firmware versions have not been verified against a device. See Fortinet's
[workspace configuration guide](https://docs.fortinet.com/document/fortimanager/7.4.3/administration-guide/908521/enable-workspace-mode).

## Selecting fields and scopes

High-level `get` calls accept `fields=["name", ...]` to request selected fields. Returned objects retain
the scope used by the request, so their later operations continue to target that scope even when the
client's selected ADOM changes. An object's explicit scope takes precedence over the request's scope.
Successful high-level GET replies with absent or null data return an empty object list.

### Device system configuration schemas

`DeviceInterface` covers all 285 interface attributes in the supplied **FortiManager 7.6.7
Configuration Database v7.4 Device Level Config** schema, including `mediatype`. It accepts both
Python names such as `snmp_index` and API names such as `snmp-index`, and writes API aliases.
IPv6 settings, DHCP client options, secondary IP entries, tagging, and VRRP accept nested dictionaries
and preserve their documented structure. Existing secondary-IP address shorthand remains supported.
`dns_server_protocol` accepts either a single protocol string or an array from FMG and normalizes
it to a list, preserving the schema's array shape when serialized.

The reference uses the same interface object definition for GET responses and ADD/SET/UPDATE
inputs and does not mark attributes read-only. Fields therefore remain optional, with no device
defaults injected into writes; a partial GET response does not need every configuration attribute.
`device` and `fmg_interface` locate the object and are excluded from its configuration payload.
The interface's API identity is `name`; `interface` is a separate parent-interface reference.
GET replies retain URL-only parent parameters from the request, including `device` and a zone's
`vdom`, so returned objects can be updated or refreshed without supplying those parameters again.
Request filters and terminal object selectors are not copied into returned configuration data.
Platform-specific availability still depends on the managed FortiGate. The schema targets FortiOS
7.4 on FMG 7.6.7; it is not evidence that every attribute exists on every 7.4 device or older FMG.

`SystemAdmin` also covers the reference's `old-password` input (`old_password` in Python).
Administrator VDOM references serialize as name arrays. `DeviceZone.tagging` accepts structured
category/name/tag rows, while its response metadata `oid` is excluded from writes because it is
not a configuration attribute in the reference. Existing attributes for older firmware remain
available even when they are absent from this particular schema.

## Waiting for tasks

Task polling works with `FMGBase` and `AsyncFMGBase` as well as the high-level clients.

Both clients accept task responses containing either `taskid` or `task` and retry transient connection
failures until the polling timeout. Async callbacks may be functions or callable objects returning an awaitable.
Failed task-creation responses and replies without task metadata are not polled; waiting returns `None`.
When a status read returns a failed response, waiting also returns `None` without invoking the progress callback.

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

## Refresh failures

`refresh()` requires a successful lookup of exactly one object. A failed lookup leaves the object
unchanged and raises a library exception, including when `raise_on_error=False`; no refreshed object
can be returned in that case.

## Transport retries and timeouts

Both clients use [pyresilience](https://pyresilience.readthedocs.io/en/latest/core/retry/) for transport
retries. JSON-RPC `get` operations retry connection failures, native timeouts, and HTTP status codes
429, 500, 502, 503, and 504. The decision uses the JSON-RPC method: every FMG request uses HTTP POST.

Login, logout, writes, and `exec` operations have one transport attempt. Replaying them after losing
a response could duplicate a completed operation. Existing authentication renewal and workspace-lock
recovery still handle explicit API rejections separately. API validation errors, malformed JSON,
certificate failures, and other HTTP errors are not retried.

Configure the same settings on `FMGSettings`, `FMG`, `FMGBase`, or their async counterparts:

| Setting | Default | Meaning |
| --- | --- | --- |
| `retry_attempts` | `3` | Total attempts per read request, including the first |
| `retry_delay` | `0.1` | Initial backoff in seconds |
| `retry_backoff` | `2.0` | Backoff multiplier |
| `retry_max_delay` | `2.0` | Backoff cap in seconds |
| `retry_jitter` | `True` | Randomize backoff delays |
| `timeout` | `120.0` | Native connect/read inactivity timeout in seconds |

Set `retry_attempts=1` to disable automatic transport retries. Exhausted transport failures retain
their native requests/aiohttp exception types. HTTP errors raise `FMGHTTPException`, whose
`status_code` attribute identifies the HTTP status. For JSON-RPC operations, `raise_on_error=False`
converts this to a failed response.

`timeout` applies to each attempt's connection and read inactivity limits, including response-body
reading. Multiple attempts and backoff can increase total elapsed time. It is not a strict overall
wall-clock deadline. The async transport uses the corresponding `aiohttp.ClientTimeout` connection
and socket limits rather than aiohttp's separate total-request timer.

The existing override works with both clients and validates positive, finite timeout values:

```python
with fmg.timeout(30):
    response = fmg.get(Address)

# When fmg is an AsyncFMG instance:
with fmg.timeout(30):
    response = await fmg.get(Address)
```

Sync requests stay on the caller's thread. pyresilience's thread-based sync timeout wrapper is not
used because it cannot reliably interrupt blocking socket I/O; see its
[timeout implementation notes](https://pyresilience.readthedocs.io/en/latest/changelog/).
Async cancellation propagates immediately. Each response is released before retrying or returning.
