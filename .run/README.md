# PyCharm test configurations

These shared pytest configurations use the project's module interpreter and `$PROJECT_DIR$`
as the working directory. Sync the development environment with `uv sync --locked`; the project
module should use `.venv` as its Python interpreter.

- **Offline tests**: all offline checks, unit-only checks, loopback transport checks, and module groups.
- **Unit test files**: each offline file can run independently.
- **Firewall modules**: individual proxy address/group, InternetService, VIP, and IP pool/group cases.
- **Lab tests**: all lab checks or a single sync/async branch.
- **Lab tests - sync / async**: each live module can run individually.

Lab configurations read `private/lab-config.yml`. They run serially and omit
`--run-baseline-tests`, so installation scenarios stay skipped unless you explicitly add that
option after authorizing the baseline procedure. Selecting a configuration does not run it.

The previous local test configurations and test files were backed up to the gitignored
`private/pycharm-tests-backup-*` directory before replacement. Non-test PyCharm configurations
were preserved. Shared `.run` files are versioned; `.idea/workspace.xml` remains local.
