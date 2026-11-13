# Advanced usage

## Compose reusable workflows

Wrap high-level operations in application functions when a workflow needs several steps.
Keep connection ownership with the caller and let failures propagate so the caller can handle them.
The following function creates a new address and group; both names must be unused.

```python
from pyfortinet import FMG
from pyfortinet.fmg_api.firewall import Address, AddressGroup


def create_backend_group(fmg: FMG, name: str, subnet: str) -> AddressGroup:
    address = Address(name=f"{name}-address", subnet=subnet)
    fmg.add(address)
    group = fmg.get_obj(AddressGroup, name=name, member=[address])
    group.add()
    return group
```

Call this function inside an open synchronous connection. These writes are separate operations:
if group creation fails, the address may remain. Define cleanup or reconciliation for your
application. Subclassing `FMG` is also possible, but custom synchronous methods are not converted
to async methods by using an asynchronous context.

## Choosing sync or async context management

`FMG` supports both connection context protocols. Use the imports and `config` from the
[quickstart](quickstart.md):

```python
with FMG(**config) as fmg:
    addresses = fmg.get(Address).data

async def read_addresses():
    async with FMG(**config) as fmg:
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
See the [developer verification notes](../developer_guide/workspace_verification.md) for the
recorded FMG 7.4.6 checks and firmware limitations.

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
Tasks completed with warnings return `"warning"`; callers can distinguish this from `"done"` and `"error"`.

During asynchronous polling, keep synchronous callbacks brief: long-running callbacks block the
event loop and delay other coroutines. For callbacks that perform I/O, use an asynchronous
function and await nonblocking operations.

### Using callbacks while waiting

To display the current completion percentage and latest log line:

```python
state = fmg.wait_for_task(task_id, callback=lambda percent, log: print(percent, log))
```

For a progress bar, install the optional Rich dependency with `pyfortinet[rich]` or
`pyfortinet[all]`. This synchronous example uses the `config` from the [quickstart](quickstart.md)
and installs device settings onto the selected firewall. Review pending configuration before
running it, and replace `branch-fw` with the intended device name.

```python
from rich.progress import Progress

from pyfortinet import FMG
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.securityconsole import InstallDeviceTask

firewall = "branch-fw"
with FMG(**config) as fmg:
    task = fmg.get_obj(
        InstallDeviceTask,
        adom=fmg.adom,
        scope=[Scope(name=firewall, vdom="root")],
        flags=["auto_lock_ws"],
    )
    result = task.exec()
    with Progress() as progress:
        prog_task = progress.add_task(f"Installing settings on {firewall}", total=100)
        state = result.wait_for_task(
            callback=lambda percent, log: progress.update(prog_task, completed=percent)
        )
    if state != "done":
        raise RuntimeError(f"Installation did not complete successfully: {state}")
```

## Connection cleanup

Malformed login replies and missing session tokens raise `FMGTokenException` in both clients.

Calling `open()` on an already open client keeps the existing session and workspace locks. To start
a new session, close the client first.

`close()` is safe before opening a connection and after it has already been closed. Both clients release
the HTTP session and clear authentication and cached workspace state even if logout fails. For async
clients, await `close()`.

Workspace commit and unlock failures are logged and raised after logout and session cleanup.
A failed commit response raises `FMGLockException`, including when `raise_on_error=False`, because
there is no response object returned from `close()` for the caller to inspect. Unlock is still
attempted when a commit fails.
If a `with` or `async with` block is already exiting with an exception, cleanup failures are logged
and the original exception continues to propagate. On normal exit, cleanup errors are raised.

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

## Filtering with F

`F` builds the filter argument for high-level `FMG.get()` and `AsyncFMG.get()` calls.
The same expressions work with both clients; only the request needs awaiting. Import the
resource class and use an open connection configured as in the [quickstart](quickstart.md):

```python
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.firewall import Address

filters = F(name__like="server%") & F(type="ipmask")
addresses = fmg.get(Address, filters=filters).data
```

Filters are sent to FortiManager, which evaluates them against the selected table. Local
construction checks the operator syntax; it does not validate field names or establish that a
particular firmware supports an operator for that field.

### One condition and comparison operators

Use `F(field=value)` for equality or `F(field__operator=value)` for an explicit comparison.
Each `F` accepts one condition. Combine separate instances for multiple conditions.

| Suffix | API operator | Example |
| --- | --- | --- |
| omitted or `eq` | `==` | `F(name="server1")` |
| `neq` | `!=` | `F(type__neq="fqdn")` |
| `lt`, `le` | `<`, `<=` | `F(color__lt=10)` |
| `gt`, `ge` | `>`, `>=` | `F(color__ge=2)` |
| `in` | `in` | `F(name__in=["server1", "server2"])` |
| `contain` | `contain` | `F(member__contain="server1")` |
| `like`, `not_like` | `like`, `!like` | `F(name__like="server%")` |
| `glob`, `not_glob` | `glob`, `!glob` | `F(name__glob="server*")` |
| `or` | `&` (bitwise test) | `F(flags__or=[3, 1])` |

`in` compares a field with several candidate values; `contain` searches a list-valued field
for a member. Choose a resource that exposes the field: for example, `member` belongs to an
address group rather than an address.

The legacy suffix `__or` maps to the API's bitwise `&`, not logical OR. The implementation
comments describe one integer target as testing `(source & target) == 0`, and two targets as
testing `(source & mask) == expected`. Verify the field and semantics against your firmware
reference before using it. Use `|` between conditions for logical OR.

Unknown suffixes and multiple conditions in one `F` raise `ValueError`. Values retain their
Python types; a list expands into separate API targets:

```python
assert F(name="server1").generate() == ["name", "==", "server1"]
assert F(name__in=["server1", "server2"]).generate() == [
    "name", "in", "server1", "server2"
]
assert F(color__ge=2).generate() == ["color", ">=", 2]
```

### API field names and separators

`F` does not look up a model's aliases. Its default `_sep="_"` preserves underscores.
For API fields with dashes, set `_sep="-"`; a leading underscore is preserved:

```python
assert F(allow_routing="enable").generate() == ["allow_routing", "==", "enable"]
assert F(allow_routing="enable", _sep="-").generate() == ["allow-routing", "==", "enable"]
assert F(_image_base64__like="data%", _sep="-").generate() == [
    "_image-base64", "like", "data%"
]
```

For fields containing spaces or other characters that cannot appear in Python keyword names,
pass the exact API name through a dictionary:

```python
assert F(**{"scope member__in": ["branch-fw"]}).generate() == [
    "scope member", "in", "branch-fw"
]
```

Use the endpoint's actual API spelling. For example, device inventory fields such as
`conn_status` retain underscores.

### AND, OR, and implicit OR lists

Use `&` for AND, `|` for explicit OR, and `+` for the API's implicit OR list.
Python `and` and `or` do not build filter expressions.

```python
assert (F(name="server1") | F(name="server2")).generate() == [
    ["name", "==", "server1"], "||", ["name", "==", "server2"]
]
assert (F(name="server1") + F(name="server2")).generate() == [
    ["name", "==", "server1"], ["name", "==", "server2"]
]

filters = (F(name="server1") | F(name="server2")) & F(type="ipmask")
assert filters.generate() == [
    [["name", "==", "server1"], "||", ["name", "==", "server2"]],
    "&&",
    ["type", "==", "ipmask"],
]
```

Parenthesize mixed expressions: Python evaluates `+` before `&`, and `&` before `|`.
Parentheses around adjacent expressions with the same operator may disappear because the
builder flattens those lists. Different operators retain their nested structure.

A tricky case from the tests combines protocol conditions with a null-or-zero check:

```python
from pyfortinet.fmg_api.firewall import ServiceCustom

filters = (F(protocol="ICMP") & F(icmptype="8")) & (F(icmpcode=None) + F(icmpcode=0))
assert filters.generate() == [
    [["protocol", "==", "ICMP"], "&&", ["icmptype", "==", "8"]],
    "&&",
    [["icmpcode", "==", None], ["icmpcode", "==", 0]],
]
services = fmg.get(ServiceCustom, filters).data
```

Here `None` remains an explicit filter target; it is not omitted like a null field in a write
payload. FortiManager decides whether a null comparison is meaningful for the selected field.

### Negation and reusable conditions

`~F(...)` negates one condition and returns a copy. Inverting it again removes the negation:

```python
online = F(conn_status="up")
offline = ~online
assert online.generate() == ["conn_status", "==", "up"]
assert offline.generate() == ["!", "conn_status", "==", "up"]
assert (~offline).generate() == online.generate()
```

Negation is implemented for individual `F` instances, not combined filter groups. To express
NOT (A OR B), negate both conditions and join them with AND:

```python
filters = ~F(name="server1") & ~F(name="server2")
```

Use `~`, not Python `not`, which produces a boolean. Composition preserves existing
expressions, so you can reuse a base condition without altering it.

### Build a filter dynamically

An empty `F()` can seed a nonempty sequence on the left of `|`, `&`, or `+`.
Handle an empty input explicitly rather than generating or sending the empty seed:

```python
hosts = ["server1", "server2"]
if not hosts:
    addresses = []  # No requested names means no lookup in this application.
else:
    filters = F()
    for host in hosts:
        filters |= F(name=host)
    addresses = fmg.get(Address, filters).data
```

Do not use the truth value of `F()` to test whether any conditions were added. Track the input
or accumulated conditions explicitly.

### Text filters

High-level GET also accepts a text expression. Use the suffix names from the operator table,
such as `eq` and `like`, with lowercase `and`, `or`, or a comma for implicit OR.
Use `text_to_filter()` to inspect the generated structure without a connection:

```python
from pyfortinet.fmg_api.common import text_to_filter

expression = "(name eq server1 or name eq server2) and type eq ipmask"
filters = text_to_filter(expression)
assert filters.generate() == (
    (F(name="server1") | F(name="server2")) & F(type="ipmask")
).generate()
addresses = fmg.get(Address, expression).data

assert text_to_filter("~name like host_%").generate() == ["!", "name", "like", "host_%"]
assert text_to_filter("name eq server1, name eq server2").generate() == [
    ["name", "==", "server1"], ["name", "==", "server2"]
]
```

The parser is deliberately small. Values are single non-whitespace tokens and remain strings;
it does not implement quoted values with spaces, Python lists, or numeric conversion.
Prefer `F(comment="Application server")`, `F(color__ge=2)`, and `F(name__in=[...])` for those cases.

Mixed unparenthesized text is parsed recursively from the right, rather than following Python's
operator precedence. For example, `name eq server1 and type eq ipmask or type eq fqdn`
groups as `name eq server1 and (type eq ipmask or type eq fqdn)`. Always use explicit parentheses
when mixing operators. Malformed expressions raise `ValueError`.

### Patterns and inspection

The operator comments describe SQL-style `like` patterns: `%` matches any sequence of characters
and `_` matches a single character. Thus `host_%` does not mean a literal underscore.
`glob` uses case-sensitive Unix-style patterns, such as `host-*`.
Use equality for a literal name containing wildcard characters.

Call `.generate()` to inspect grouping, field spelling, and value types. It only builds a local
list and makes no request. The examples above follow the offline common/filter composition
tests; endpoint-specific matching still requires a compatible FortiManager.

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

The override works with both clients and validates positive, finite timeout values. Async overrides
are local to the current task's context, so overlapping tasks can use different values on the same
client. Nested blocks restore the previous override on exit, including when an exception occurs:

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
