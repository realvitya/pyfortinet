# Test guide

## Testing config file

It is advisable to put all lab related configs and files to a separate folder which is not part of the GIT repository.
I used to use private folder which is excepted from GIT. In that folder you can store your config files. One of the most
important config file is `lab-config.yml`. This file contains access to your lab environment.

Example of `lab-config.yml` file:

```yaml
---
fmg:
  base_url: https://myfmg.co.com/
  verify: false
  username: admin
  password: verysecret
  adom: root
```

## Offline regression tests

Run `uv run pytest tests/unit` (or `pytest tests/unit` in an activated environment) to check shared sync
and async behavior without a lab configuration or network access.
These tests mock the transport and exercise the public client methods.

## Async test event loops

The development dependencies require pytest-asyncio 0.24 or newer. Pytest uses auto mode and defaults async
fixtures to function-scoped event loops. `AsyncTestCase` uses function-scoped connections and resources, so setup,
requests, cleanup, and logout run on the same loop. Only the connection explicitly requested by a test is opened.

## Live test isolation and cleanup

For high-level model responses, `response[value, "field"]` raises `AttributeError` if the model has no such
attribute. A valid field with no matching value returns `None`, including an unset optional field.
Sync and async responses share this behavior. Raw dictionary lookups retain their existing permissive behavior;
they do not have a model schema for validating field names.

GET treats an absent object as a successful empty lookup. Low-level clients return
`success=True` and `data=[{"data": [], "status": {"code": 0}}]`, consistently with the normal result-list shape.
This replaces the previous inconsistent `success=False` and bare dictionary for missing objects.
High-level callers receive an empty object list and `.first()` returns `None`.
Request success and object presence are separate checks; permission, transport, and malformed-response errors
remain errors and must never be interpreted as absence.

Each live test owns its setup and cleanup. Low-level address CRUD steps form one lifecycle test rather than
depending on earlier test methods. Request `lab` (high-level) or `base_lab` (low-level) to register resources before
writing them. `lab.object(Model, "label", **fields)` creates a bound model with a per-test name and reserves its
delete URL; it does not add the object. Async tests await this method. Labels are at most six alphanumeric characters.
For raw requests, call `reserve(url)` before the write. Existing resources are rejected, never adopted or deleted.
Legacy batch scenarios retain fixed names but check absence before use.

Teardown checks and deletes owned resources in reverse registration order, verifies absence, and attempts remaining
cleanup even if one operation fails. Register parents before children (addresses before groups, interfaces before
zones). Cleanup runs before logout and also after failed assertions or partially successful writes. Failures identify
the remaining resource URLs without printing raw transport exceptions. `lab.wait(response)` tracks unfinished tasks;
device deletion uses its command API and waits for completion. Workspace discard is an additional safeguard.

The audit found these previous leak paths:

| Tests                              | Previous risk                                                 | Organization now                            |
|------------------------------------|---------------------------------------------------------------|---------------------------------------------|
| Low-level address CRUD             | Ordered methods and a final cleanup test                      | One lifecycle with failure-path teardown    |
| Firewall mapping, groups, services | Server mapping, third member, service left behind             | Owned resource journal                      |
| Normalized interfaces              | Replaced an existing `TEST` object                            | Unique owned interface                      |
| VLAN, zone, administrator          | Objects left behind; first device selected                    | Explicit FG01 and reverse cleanup           |
| Device and ADOM lifecycle          | Fixed-name collision, existing ADOM deletion, unfinished jobs | Unique names and task-aware cleanup         |
| Batch operations                   | Partial writes bypassed final deletes                         | Reservation before the first write          |
| Authentication fault injection     | Lost real session token or URL prevented logout               | Mocked unit coverage; live login smoke only |
| Installation                       | Changed description and installed device configuration        | No description mutation; baseline-only test |

The async directory now uses actual async clients for system, policy, dynamic interface, and installation checks.
Duplicate scenarios were consolidated; a lower collected test count does not mean the CRUD steps were removed.

Install tests carry `requires_baseline` and are skipped unless `--run-baseline-tests` is supplied with an explicitly
authorized baseline and restore procedure. They can install unrelated pending settings, so object cleanup cannot
make them atomic. Restore the authorized snapshot after these tests; the suite does not automate Hyper-V restoration.

Cleanup is compensating work, not a database transaction. A killed process, unreachable device, or a task completing
after a timeout can still leave state behind. Inspect reported resources and restore the authorized baseline when
needed. Do not rerun failed writes blindly. The new cleanup paths require live firmware verification before claiming
that the entire lab is restored after every failure.

## Local transport checks

Run `uv run pytest tests/transport` to verify native HTTP timeouts against a temporary loopback-only TCP peer.
These tests need permission to create local sockets and do not connect to a FortiManager device.
