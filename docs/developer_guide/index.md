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
uv run invoke docs-serve
uv run invoke docs
```

Documentation builds require **Python 3.11 or later**. The library and its runtime dependencies
continue to support Python 3.9. On Python 3.9/3.10, the development extra and group omit Zensical
and its Python handler. Use a separate clone or virtual environment with Python 3.11+ for docs;
for example, run `uv sync --locked --python 3.11` in a dedicated checkout. The pip alternative is
`python -m pip install -r docs/requirements.txt` using Python 3.11+.

The Invoke tasks first run the independent `docs/gen_ref_pages.py` generator, then invoke
`zensical serve` or `zensical build --strict`. Run them from the repository root.
The generator writes ignored Markdown under `docs/reference/`, preserves the published module
paths and identifiers, and removes stale generated pages after source files are renamed or removed.
It refuses to overwrite Markdown it does not own. Restart `docs-serve` after adding, renaming, or
removing source modules so the generated page list and navigation are refreshed.

For a direct build without Invoke:

```shell
uv run python docs/gen_ref_pages.py
uv run zensical build --strict
```

Keep `mkdocs.yml`: Zensical supports that configuration format. The `classic` theme variant
preserves the Material appearance. Search, cross-references, section indexes, and literate
navigation use Zensical's compatibility implementations; `gen-files` is no longer used.
The old Invoke task names `mkdocs` and `mkdocs-serve` remain aliases. The old
`--push-to-github` flag is removed; local documentation commands do not deploy.

### GitHub Pages

The documentation workflow builds pull requests and uploads a site artifact. Pushes to `master`
and manual workflow runs also deploy it using the official Pages actions. Changes to docstrings,
Markdown, configuration, dependencies, and documentation tasks all trigger a build.
Before the first deployment, configure the repository's **Settings ? Pages ? Source** to
**GitHub Actions**. This migration does not change that remote setting automatically.
See the [Zensical publishing guide](https://zensical.org/docs/publish-your-site/).

### Documentation sources

Maintain both documentation layers:

- User pages explain workflows using high-level objects, prerequisites, and expected results.
- Developer pages explain implementation, testing, schema sources, and verification limits.
- Google-style docstrings describe classes and methods with concise examples. Zensical renders
  the code reference with mkdocstrings; do not maintain a separate copy of the reference.

When public behavior changes, update the relevant examples and docstrings together.
Use the [API object guide](fmg_api_objects.md) to add a model. Keep raw request construction in
implementation or extension examples where it is needed to explain unsupported functionality.

## Build a package locally

```shell
uv build
```

Building does not publish a release. Publishing packages and deploying documentation are separate
maintainer operations.
