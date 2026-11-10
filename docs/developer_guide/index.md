# Developer guide

This guide covers contributing models, maintaining the clients, and verifying changes.
For application examples, start with the [user guide](../user_guide/quickstart.md).

## Set up a development environment

Fork and clone the repository, then run these commands from its root:

```shell
git clone https://github.com/YOURFORK/pyfortinet.git
cd pyfortinet
uv sync --locked
uv run pytest tests/unit
uv run invoke --list
```

uv installs the project in editable mode and includes the default development dependency group.
Use `uv sync` when intentionally changing dependencies and include the updated `uv.lock`.
Keep the published `dev` extra and development dependency group aligned.

The Flit build backend and pip development extra are also supported:

```shell
python -m pip install -e ".[dev]"
```

Preserve the project's Python 3.9 minimum version. Follow the existing module structure and keep
synchronous and asynchronous behavior consistent.

## Verify changes

Run focused unit tests during development. For client behavior changes, run the unit suite;
for HTTP timeout or transport changes, also run the loopback transport tests:

```shell
uv run pytest tests/unit
uv run pytest tests/transport
```

Check changed Python files with `uv run ruff check <files>` and
`uv run ruff format --check <files>`. For broader checks, use
`uv run pre-commit run --files <files>` and inspect any changes made by hooks.

Default `uv run pytest` and `uv run invoke test` select offline checks. Selecting `tests`
explicitly also includes live tests. Read the [testing guide](testing.md) and
[lab setup guide](lab_setup.md) before an authorized live run.

## Preview and build documentation

```shell
uv run mkdocs serve
uv run mkdocs build
```

Maintain both documentation layers:

- User pages explain workflows using high-level objects, prerequisites, and expected results.
- Developer pages explain implementation, testing, schema sources, and verification limits.
- Google-style docstrings describe classes and methods with concise examples. MkDocs generates
  the code reference from those docstrings; do not maintain a separate copy of the reference.

When public behavior changes, update the relevant examples and docstrings together.
Use the [API object guide](fmg_api_objects.md) to add a model. Keep raw request construction in
implementation or extension examples where it is needed to explain unsupported functionality.

## Build a package locally

```shell
uv build
```

Building does not publish a release. Publishing packages and deploying documentation are separate
maintainer operations.
