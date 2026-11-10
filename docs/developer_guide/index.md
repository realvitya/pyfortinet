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

Keep `mkdocs.yml`: Zensical supports that configuration format. This project uses the `modern`
theme variant. The `classic` variant is available for sites that prefer the previous Material
appearance; it is not required for this project.

Both variants share the same HTML structure. Changing the variant does not change page URLs,
API identifiers, Python requirements, or the publishing workflow. The project's custom CSS
still applies, but check desktop and mobile layouts after theme changes or upgrades because
visual styling can differ. See the [Zensical theme variant guidance](https://zensical.org/docs/compatibility/mkdocs/migration/#theme-variant).

Search, cross-references, section indexes, and literate navigation use Zensical's compatibility
implementations; `gen-files` is no longer used.
The old Invoke task names `mkdocs` and `mkdocs-serve` remain aliases. The old
`--push-to-github` flag is removed; local documentation commands do not deploy.

### GitHub Pages

The documentation workflow builds source on Python 3.11 and validates pull requests. Pushes to
`master`, and manual runs selecting `master`, publish the generated `site/` contents to the
`gh-pages` branch. Pull requests and manual runs on other branches only build and test; they
cannot execute the credential or publication steps. Publication preserves the branch history
while replacing obsolete generated files. The publishing action adds `.nojekyll` to bypass Jekyll.

`gh-pages` remains generated output, not a source checkout. GitHub's branch-based Pages workflow
publishes that branch. Keep the `github-pages` environment restricted to `gh-pages`; the source
build job does not enter that environment or deploy an artifact directly from `master`.

Configure the repository before publishing:

1. In **Settings > Pages > Build and deployment**, select **Deploy from a branch**, then
   **gh-pages** and **/(root)**. Do not select **GitHub Actions** for this branch-output workflow.
2. In **Settings > Environments > github-pages**, keep the existing `gh-pages` deployment rule.
3. Create a dedicated SSH deploy key following the
   [publishing action's key setup instructions](https://github.com/peaceiris/actions-gh-pages#%EF%B8%8F-create-ssh-deploy-key).
   Add its public key under **Settings > Deploy keys** with **Allow write access**. Store its
   private key under **Settings > Secrets and variables > Actions > Repository secrets** as
   `DOCS_DEPLOY_KEY`. Keep the key files outside the repository and never include the private key
   in logs or commits. A deploy key grants write access to this repository, not just `gh-pages`;
   repository rules must permit its publishing push.
4. If Actions are restricted, allow `actions/checkout`, `astral-sh/setup-uv`, and
   `peaceiris/actions-gh-pages`. No broader default `GITHUB_TOKEN` write permission is needed.

A deploy key is used because GitHub documents that pushes made with `GITHUB_TOKEN` do not
trigger a Pages build. This workflow makes a normal authenticated push, allowing GitHub's
Pages publisher to deploy from the permitted branch. See
[GitHub's publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
Remote Pages settings and credentials are not changed by editing or locally testing this workflow.

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
