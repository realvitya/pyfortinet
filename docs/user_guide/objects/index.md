# Object guides

Choose the domain that matches your task. These guides use the implemented Python models;
the generated code reference provides their full field lists and docstrings.

| Domain | Classes and workflows |
| --- | --- |
| [Firewall objects](../firewall_objects.md) | Addresses, groups, services, security profile groups, proxy objects, VIPs, IP pools |
| [Devices and ADOMs](dvmdb.md) | `ADOM`, `Device`, `VDOM`, nested `HASlave` records |
| [Policies and packages](policy.md) | `PolicyPackage`, `PackageSettings`, `Policy` |
| [Normalized interfaces](dynamic.md) | `NormalizedInterface`, nested `DynamicMapping` and `PlatformMapping` |
| [Device system settings](system.md) | `DeviceInterface`, `DeviceZone`, `SystemAdmin` |
| [Device operations](device_operations.md) | `DeviceCommand`, `DeviceTask` |
| [Tasks and installation](tasks.md) | `Task`, `TaskLine`, `TaskLineHistory`, `InstallDeviceTask` |

## Run the examples

Configure a connection using the [quickstart](../quickstart.md). Unless a context is shown, run
request snippets inside `with FMG(**config) as fmg:`. With an asynchronous client, await requests,
bound object operations, and task polling. Model construction and `get_obj()` remain synchronous.

Replace names with explicit targets in your selected ADOM. Read examples do not write configuration.
Examples using ADD, UPDATE, SET, DELETE, or EXEC change state as described on their page.
Constructing a model alone makes no API request. Referenced objects must already exist unless the
example creates them.

The examples are checked locally against models and request construction. They were not run on
a live device for this documentation update. Field availability depends on the target firmware and
platform; model validation alone does not prove device compatibility.

## Scope and coverage

Device system models operate on FortiManager's managed-device configuration database.
They do not establish a direct FortiGate connection. Saving database changes and installing them
onto a FortiGate are separate operations.

Nested data models are not necessarily independent resources. Use them in their parent objects
or inspect them in responses as documented. The `pm_config_cli` module is currently a placeholder
and has no implemented high-level CLI-template classes.
