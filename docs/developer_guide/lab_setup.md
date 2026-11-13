# Lab setup for testing

Offline unit tests and loopback transport tests do not require a FortiManager lab. Live tests
require an explicitly authorized, disposable environment and a reviewed set of operations.
See the [testing guide](testing.md) for configuration and commands.

## Prepare a lab

Use dedicated FortiManager and FortiGate instances that can be restored to a known baseline.
Virtual machines are suitable; on Windows, Hyper-V checkpoints can support restoration.
Ensure the test machine can reach FortiManager and the lab devices can communicate as required.

Record the expected firmware, ADOMs, device names, serial numbers, permitted operations, and
baseline restore procedure before running live scenarios. A separate ADOM does not isolate
administrator changes, device lifecycle operations, or configuration installations.

## Configure FortiManager

A dedicated test ADOM with normal workspace mode is recommended. Confirm that the test account
has JSON-RPC API access and permissions for the selected operations. Workflow session creation
and approval are not covered by the client locking helpers.

Store credentials locally in the gitignored `private/lab-config.yml`, using the format in the
[testing guide](testing.md#testing_config_file). Prefer certificate verification; disable it only
when explicitly intended for the lab.

## Plan cleanup and restoration

Workspace discard is an additional safeguard for uncommitted database changes. It does not
reverse every API operation or an installation onto a FortiGate. Live tests register owned
resources and attempt compensating cleanup; interrupted execution or cleanup failures can still
leave changes behind.

Review the selected tests, run live sessions serially, and inspect cleanup failures. Installation
tests require explicit baseline authorization and `--run-baseline-tests`. Restore the baseline
only through the authorized procedure.
