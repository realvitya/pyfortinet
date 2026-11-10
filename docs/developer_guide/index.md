# Developer Guide

First, thank you for being interested in developing this library! The following topics tries to describe the intended
setup and workflow to develop the library!

## Installing dev tools

For development with [uv](https://docs.astral.sh/uv/), sync the project and its default development group:

```shell
git clone https://github.com/{YOURFORK}/pyfortinet.git
cd pyfortinet
uv sync
uv run pytest tests/unit
uv run invoke --list
uv build
```

PyCharm configurations in `.run/` separate offline module/file runs from the live `tests/lab`
tree. See the [test guide](testing.md) for the layout and commands. `uv run invoke test` runs
offline checks; `uv run invoke lab-test` selects live scenarios explicitly.

`uv sync` installs the project in editable mode. Commit `uv.lock` when dependency changes update it;
use `uv sync --locked` to require the checked-in resolution. `uv sync --no-dev` installs runtime
dependencies only; add `--extra async`, `--extra rich`, or `--extra all` as needed.

The Flit build backend and the existing pip development extra remain supported:

```shell
# clone your fork
git clone https://github.com/{YOURFORK}/pyfortinet.git
# install in edit mode
pip install -e ./pyfortinet[dev]
```

## Using Invoke

The project uses [Invoke](https://www.pyinvoke.org/) for common tasks. You may check all tasks supported in the
`tasks.py` config file.

### Run linters

Linters are invoked by pre-commit which is installed with the dev tools.

### Start mkdocs server
