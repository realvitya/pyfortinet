# From FortiManager API calls to Python objects

If you already use [How to FortiManager API](https://how-to-fortimanager-api.readthedocs.io/en/latest/),
the underlying concepts remain familiar: ADOMs, configuration objects, policy packages, workspace
locks, and asynchronous tasks. pyfortinet represents supported resources as Python models and
handles request construction, authentication, and response conversion.

The external guide explains the JSON-RPC API and covers more endpoints than pyfortinet currently
models. Use it for API context and Fortinet's firmware-specific reference for field and route
definitions. Use this guide for workflows built with the implemented high-level classes.

## Translate operations into object methods

| API concept | High-level Python API |
| --- | --- |
| Login, session token, logout | `with FMG(**config) as fmg:` |
| ADOM portion of an object URL | `adom` in connection settings or an explicit object scope |
| GET an object table | `fmg.get(Address).data` |
| Select an address by name | `fmg.get(Address(name="server1")).first()` |
| Filter expressions | `F(...)` combined with `&`, `\|`, and `~` |
| ADD a configuration object | `fmg.add(Address(name="server1", subnet="192.0.2.1/32"))` |
| UPDATE selected fields | `fmg.update(Address(name="server1", comment="Application server"))` |
| DELETE an identified object | `fmg.delete(Address(name="server1"))` |
| Device-specific override | A model's `dynamic_mapping` and `Scope` |
| Execute an operation | `fmg.exec(task)` or a bound task's `.exec()` |
| Poll a returned task ID | `response.wait_for_task()` |

## Models, bound objects, and responses

`Address(...)` creates a local Pydantic model. It validates supported fields but makes no API call.
`fmg.get_obj(Address, name="server1")` constructs a model bound to a client, also without an API call.
Binding an existing instance with `fmg.get_obj(address)` returns that same instance.
Neither operation fetches the object's configuration.

Call `fmg.get(...)` to read configuration. High-level GET responses contain typed models in
`.data`; the returned models are bound to the requesting client. This enables methods such as
`.refresh()`, `.update()`, and `.delete()`. With an asynchronous client, await these methods.

`.success` and the response's truth value describe request success. They do not indicate whether
a GET found an object: a successful empty lookup has `.data == []` and `.first() is None`.
Write and execution responses do not necessarily contain a typed object. Read or refresh the
object when you need FortiManager's resulting configuration.

## Scope and policy packages

Choose an ADOM explicitly when connecting. The settings default is `global`, which refers to
the Global Database. An explicit object's `fmg_scope` takes precedence over the connection's
selected ADOM. Fetched objects retain their request scope even if `fmg.adom` later changes.

Policy objects also require a policy package, abbreviated PP. Inside an open connection, read
the policies in an existing package:

```python
from pyfortinet.fmg_api.policy import Policy

policies = fmg.get(Policy(pkg="branch-policy")).data
for policy in policies:
    print(policy.policyid, policy.name)
```

Replace `branch-policy` with a package in your selected ADOM. The model constructs its URL;
you do not need to assemble a `/pm/config/...` path.

## Write, commit, and install are separate steps

An object write changes FortiManager's database. With workspace enabled, the client can acquire
ADOM locks in response to a lock-required API error. Explicit locking is also available.
Normal connection cleanup attempts to commit workspaces locked by that client and release locks.
`discard_on_close=True` skips those commits; `discard_on_error=True` is the default when an
exception leaves the context. Neither setting reverses an installation or every device operation.

An installation task applies configuration to selected managed devices. Its successful creation
does not establish that installation has completed. Keep the connection open, wait for the task,
and check its terminal state. See the [installation how-to](howto.md#install_device_settings_and_wait_for_completion).

## Coverage and extension

The [object guides](objects/index.md) organize supported models by domain.
The generated code reference describes their complete field lists. Model validation does not
guarantee that every firmware or device platform accepts every field. `_version` metadata does
not enforce firmware compatibility.

When a resource has no model, low-level clients and dictionary requests remain available.
For reusable workflows, consider contributing a model using the
[API object implementation guide](../developer_guide/fmg_api_objects.md), so callers can continue
working with Python objects.
