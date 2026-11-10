# Implementing API objects

High-level models translate FortiManager resources into validated Python objects. Read the
relevant implementation and tests before adding a route. Check Fortinet documentation for
the target FMG firmware and managed FortiOS version; record the source and verification limits.

## Choose the domain and base class

Place a model in the module matching its API domain. Firewall models live in
`pyfortinet/fmg_api/firewall/`; export public classes through its explicit `__all__` in
`__init__.py`. Keep shared normalization in `_values.py` and literal choices in `types.py`.
Import literal choices from `firewall.types` and `PORT_RANGE_TYPE` from `firewall.service`;
the firewall package root exports classes.

Use `FMGObject` for configuration resources and `FMGExecObject` for execution operations.
The base classes provide client binding and operation delegation. Keep transport handling in
the synchronous and asynchronous clients; share pure request or normalization helpers where useful.

## Define fields, aliases, and identity

The following is an illustrative template, not an implemented FortiManager endpoint:

```python
from typing import Optional

from pydantic import AliasChoices, Field

from pyfortinet.fmg_api import FMGObject


class ExampleObject(FMGObject):
    """Illustrative configuration model.

    Attributes:
        name: Object name used for item operations.
        display_name: Optional descriptive name.
    """

    _url = "/pm/config/{scope}/obj/example/{entry}"
    _master_keys = {"entry": "name"}

    name: Optional[str] = None
    display_name: Optional[str] = Field(
        None,
        validation_alias=AliasChoices("display-name", "display_name"),
        serialization_alias="display-name",
    )
```

`_master_keys` maps URL placeholders to model fields; it is a dictionary, not a list.
Match the documented API identity. Most model fields, including identity fields on collection
models, should default to `None` so collection GETs, partial replies, and partial updates work.
An item operation still requires enough information to identify its target. Require a field at
construction only when the model cannot represent a valid supported operation without it.

`Optional[str]` alone allows null values but does not make a Pydantic 2 field optional at
construction. Supply a default, usually `None`, when omission is supported.

Accept Python names and API aliases with `AliasChoices` and serialize with the API spelling.
High-level writes use `model_dump(by_alias=True, exclude_none=True)`; they do not exclude every
explicit default or unchanged field. Avoid injecting device defaults into partial writes.

Use `Field(..., exclude=True)` or an optional excluded field for URL-only parameters and response
metadata that must not appear in configuration payloads. Follow existing model conventions and
the firmware reference rather than assuming all returned attributes are writable.

## Construct URLs and scopes

`get_url(method=...)` is a method, not a property. The default implementation replaces
`{scope}` with `global` or `adom/<name>`, resolves URL fields, and handles terminal selectors
according to the operation. Inspect existing models and request tests before overriding it.

Directly constructed models have no scope unless `fmg_scope` is supplied. High-level client
operations supply the selected connection scope when needed. Explicit object scope takes
precedence. Returned models retain request scope and URL-only parent fields so later updates
and refreshes can reach the same resource.

For package-scoped objects, follow `Policy`, whose URL includes `{adom}`, `{pkg}`, and
`{policy}` and maps the policy selector to `policyid`. Keep `pkg` out of the configuration payload. Do not replace `get_url` with a
property or assume every route uses a terminal name selector.

`_version` is descriptive metadata; it does not currently enforce minimum firmware versions.

## Validate and serialize values

Use Pydantic validators for supported normalization, such as API integer choices to Python
literals. Map values according to the firmware schema; do not infer an enumeration from an
unrelated endpoint. Keep invalid input visible as a validation error.

When an API field references other objects by name, accept the supported names or model types
and serialize references as name arrays. Passing a referenced model must not implicitly create it.
Use separate nested models when mapping fields differ from parent fields.

Preserve the distinction between an unset collection (`None`, omitted from writes) and an
explicit empty collection (`[]`, sent to the API). Keep synchronous and asynchronous behavior
consistent, including aliases and normalization.

## Verify an implementation

Add offline regression tests in the matching `tests/unit/` domain. Cover construction with Python
names and API aliases, normalization, serialization, URL assembly, scope, partial responses, and
meaningful invalid inputs. Mock external transport for client behavior. Check both clients when
the behavior affects request handling.

Live verification is separate and requires authorization. Register cleanup before writes, refuse
pre-existing test resources, and keep each test independent. See the [testing guide](testing.md)
for fixtures, baseline requirements, and cleanup limitations.

## Document and review

Use Google-style class and method docstrings with concise, valid examples. Explain identifiers,
URL-only fields, supported operations, and relevant serialization behavior. Add user-facing
workflows to the user guide and schema or firmware verification details to the developer guide.

Run the focused tests, Ruff checks for changed Python files, and `uv run invoke docs` (Python 3.11+).
Document unavailable firmware references or device verification explicitly. Do not claim runtime
support merely because a schema-backed model validates locally.
