# Test guide

## Test trees and PyCharm

```text
tests/
  unit/                  # Offline tests, grouped by module
    client/
    common/
    dynamic/
    firewall/
    lab_helpers/         # Cleanup infrastructure tested with mocks
    policy/
    system/
    fixtures/            # Frozen schema references
  transport/             # Offline loopback HTTP checks
  lab/                   # Live FMG scenarios
    sync/
      objects/
    async/
      objects/
    fixtures.py          # Function-scoped live connections
    resources.py         # Ownership and compensating cleanup
```

Default pytest discovery selects `tests/unit` and `tests/transport`. Live connection fixtures and
credential loading are confined to `tests/lab`; offline tests do not load the lab configuration.
All paths below are relative to the repository root.

```powershell
uv sync --locked
uv run pytest tests/unit tests/transport
uv run pytest tests/unit/firewall
uv run pytest tests/unit/firewall/test_service_ports.py
uv run invoke test
uv run invoke test --module unit
```

PyCharm loads shared configurations from `.run/`. The **Offline tests**, **Unit test files**, and
**Firewall modules** folders provide combined, module-level, per-file, and per-firewall-family runs.
The **Lab tests**, **Lab tests - sync**, and **Lab tests - async** folders target only the live tree.
Configurations use the module's interpreter (the project's `.venv`) and the repository root as the
working directory. Lab configurations pass `--lab_config private/lab-config.yml`. Regular lab
configurations omit the baseline option; **Lab - all - with baseline** explicitly enables
`--run-baseline-tests` for an authorized baseline/installation run. Configuration checks use
targets and display names, so filenames can be renamed. Reopen the project if the IDE has not yet
refreshed the shared configuration list.

The previous `.idea` state and test files were backed up locally under
`private/pycharm-tests-backup-*` before replacement. This backup is gitignored and may contain
local IDE settings. With PyCharm closed, restore its `.idea/workspace.xml` to recover the old local
run entries, and move the generated `.run` directory aside if you want to hide the new shared entries.
Non-test run configurations were preserved.

After reviewing and authorizing the selected lab operations, run a live module or branch serially:

```powershell
uv run pytest tests/lab/sync/objects/test_firewall_extended.py --lab_config private/lab-config.yml -ra
uv run invoke lab-test --module async
```

`invoke lab-test --baseline` additionally enables installation scenarios and requires the authorized
baseline/restore procedure. `invoke test` runs offline checks only.

## Testing config file

Store lab configuration and credentials in the gitignored `private/` directory.
Keep `private/lab-config.yml` local and never include credentials in diagnostics or commits.
Prefer certificate verification; set `verify: false` only when explicitly intended for the lab.

Example of `lab-config.yml` file:

```yaml
---
fmg:
  base_url: https://myfmg.co.com/
  verify: true
  username: admin
  password: "<lab-password>"
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

## Additional firewall lab scenarios

The following files contain 16 independent live scenarios (eight synchronous and eight asynchronous)
for the schema-backed firewall objects:

- `tests/lab/sync/objects/test_firewall_extended.py`
- `tests/lab/async/objects/test_async_firewall_extended.py`

| Objects | Coverage |
|---------|----------|
| ProxyAddress, VIP, IPPool | Add, read, update, refresh, set, delete, verify absence |
| ProxyAddressGroup | Owned members, add/read, clone, membership update/set, delete |
| IPPoolGroup | Owned CGN pools, add/read, exclusive-membership clone rejection, update/set, delete |
| VIP, IPPool dynamic mappings | Add scoped override, read typed mapping, change override, remove mapping |
| InternetService | Bounded read of one catalog record followed by a high-level ID-filtered lookup |

These tests refuse an ADOM other than `test`. Mapping scenarios require the existing `FG01` device,
its `root` VDOM, and `port1` for the VIP interface override. They do not install configuration, create
devices/ADOMs, change workspace mode, or modify pre-existing objects. Every created or cloned object
is reserved with `lab` before its write. Member resources are registered before groups, so teardown
removes references before their parents. Cleanup also runs after a failed assertion or partial write.
The catalog test makes no writes and skips explicitly if the Internet Service Database is empty.

The implementation reference is FMG 7.6.7 with FortiOS 7.4 ADOM objects. The lab must support the
selected endpoints and fields; older firmware or a missing feature may fail a scenario. These new
scenarios were exercised on FMG 7.4.6 build 2588. IP pool groups require CGN resource-allocation
pools and reject cloning a populated group because pools cannot belong to two groups. The tests
check that specific rejection and verify that no clone was created. FMG 7.6.7 itself remains
unverified. After authorizing their object writes, run the scenarios serially:

```powershell
uv run pytest tests/lab/sync/objects/test_firewall_extended.py tests/lab/async/objects/test_async_firewall_extended.py --lab_config private/lab-config.yml -ra
```

For collection without a lab connection, add `--collect-only` and use a nonexistent config path.

The verified FMG 7.4.6 run completed with **14 passed and 2 skipped**: the catalog count was zero,
so both InternetService lookups skipped. Cleanup verification found no remaining journaled objects,
the five object-table name inventories matched their pre-run baseline, and ADOM `test` had no
workspace lock records. No configuration was installed.

## Local transport checks

Run `uv run pytest tests/transport` to verify native HTTP timeouts against a temporary loopback-only TCP peer.
These tests need permission to create local sockets and do not connect to a FortiManager device.
