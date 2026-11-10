# Policies and packages

The `policy` module models policy packages (PPs) and the policies within them.
Use an explicit ADOM and the connection conventions in the [object guide](index.md).

## PolicyPackage

Read packages in the selected scope, or select an existing package by name:

```python
from pyfortinet.fmg_api.policy import PolicyPackage

packages = fmg.get(PolicyPackage).data
package = fmg.get(PolicyPackage(name="branch-policy")).first()
for item in packages:
    print(item.name, item.type)
```

The model's `name` field identifies a package; `scope_member` describes its assigned devices
and VDOMs. Folder handling is not fully tested, so these examples use a package without parent
folders.

## PackageSettings

`PackageSettings` is embedded in a policy package, not added independently.
This example creates a new package assigned to an existing device and VDOM:

```python
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.policy import PackageSettings, PolicyPackage

package = PolicyPackage(
    name="example-branch-policy",
    scope_member=[Scope(name="branch-fw", vdom="root")],
    package_settings=PackageSettings(fwpolicy_implicit_log="enable"),
)
fmg.add(package)
```

The package name must be unused. Assigning a package and creating its database record do not
install it onto the device. `InstallDeviceTask` is for device settings; this library currently
has no dedicated high-level policy-package installation task.

## Policy

Supply `pkg` to locate the package and `policyid` when selecting an individual policy.
The connection supplies the ADOM unless the model has an explicit `adom`.

```python
from pyfortinet.fmg_api.policy import Policy

policies = fmg.get(Policy(pkg="branch-policy")).data
policy = fmg.get(Policy(pkg="branch-policy", policyid=10)).first()
for item in policies:
    print(item.policyid, item.name, item.action)
```

To update one field on an existing policy:

```python
fmg.update(Policy(pkg="branch-policy", policyid=10, comments="Reviewed branch rule"))
```

`pkg` and `adom` locate the resource and are excluded from the configuration payload.
Address and service references accept names or supported named firewall models. Supplying
a referenced model does not create it.

The following constructs a local rule for inspection. It does not write the rule:

```python
from pyfortinet.fmg_api.firewall import Address, ServiceCustom

rule = Policy(
    pkg="branch-policy",
    name="Example application access",
    srcintf=["lan"],
    dstintf=["wan"],
    srcaddr=[Address(name="example-network")],
    dstaddr=["all"],
    service=[ServiceCustom(name="example-web")],
    action="accept",
    schedule=["always"],
    logtraffic="all",
)
payload = rule.model_dump(by_alias=True, exclude_none=True)
assert payload["srcaddr"] == ["example-network"]
assert payload["service"] == ["example-web"]
assert "pkg" not in payload
```

Before adding a rule, confirm that the package, interfaces, addresses, services, and schedule
exist, and review the intended policy placement. This example does not claim automatic ordering
or package installation.
