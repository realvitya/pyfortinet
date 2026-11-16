# Workspace verification notes

These recorded checks describe workspace discovery and Global Database locking on FMG 7.4.6.
They are historical verification evidence, not a verification run for this documentation change.

Workspace discovery and locking were verified on FMG 7.4.6 build 2588 by temporarily changing global mode and the
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

