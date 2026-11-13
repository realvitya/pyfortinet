# Installation

pyfortinet requires Python 3.9 or later and Pydantic 2. Use a virtual environment to keep its
dependencies separate from other applications.

## Install with uv

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first if it is not already
available. For an application that uses pyfortinet, create a project and add the dependency:

```shell
uv init fortimanager-automation
cd fortimanager-automation
uv add pyfortinet
```

For asynchronous support, use this dependency instead:

```shell
uv add "pyfortinet[async]"
```

Save an example as `main.py` and run it in the project environment:

```shell
uv run python main.py
```

uv manages the project's virtual environment and dependency lockfile. Activation is unnecessary
when using `uv run`. See the [uv project guide](https://docs.astral.sh/uv/guides/projects/)
for details.

### Use uv with a standalone virtual environment

For a script directory without a uv project, use the
[uv pip interface](https://docs.astral.sh/uv/pip/environments/):

```shell
uv venv
uv pip install "pyfortinet[all]"
```

Activate `.venv` using the platform-specific commands in the pip section below, then run your
script with `python main.py`. `uv pip install` installs into the discovered environment;
it does not add a dependency to `pyproject.toml` or maintain a project lockfile.

### Work on pyfortinet itself

For this repository, use its checked-in dependency resolution instead of creating a new project:

```shell
git clone https://github.com/realvitya/pyfortinet.git
cd pyfortinet
uv sync --locked
uv run invoke docs-serve
```

The default development group includes optional client dependencies and, on Python 3.11+,
the Zensical documentation tools. Building or previewing docs requires Python 3.11+;
using the library still requires only Python 3.9+.
For a runtime-only source environment, use `uv sync --locked --no-dev`, adding
`--extra async`, `--extra rich`, or `--extra all` as needed.
See the [developer guide](../developer_guide/index.md) for contribution checks.

## Install with pip

```shell
python -m venv .venv
```

Activate it on Linux or macOS:

```shell
source .venv/bin/activate
```

Or in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install the package:

```shell
python -m pip install pyfortinet
```

| Installation | Includes |
| --- | --- |
| `pyfortinet` | Synchronous clients and object models |
| `pyfortinet[async]` | Adds aiohttp for asynchronous clients |
| `pyfortinet[rich]` | Adds Rich for optional formatted output |
| `pyfortinet[all]` | Adds both optional dependencies |

Quote extras when installing from a shell:

```shell
python -m pip install "pyfortinet[async]"
```

## Connect to FortiManager

Use the FortiManager HTTPS URL, an account with JSON-RPC API access, and an explicit ADOM.
The client appends `/jsonrpc` if absent from `base_url`. Username/password authentication is
currently supported. Direct FortiGate connections are not implemented.

Certificate verification defaults to `True`. For the synchronous requests transport,
`REQUESTS_CA_BUNDLE` can identify a trusted CA bundle. That setting is specific to requests;
do not assume it configures aiohttp. For asynchronous clients, ensure the certificate is trusted
by the Python SSL environment. `verify=False` disables certificate verification and should be
limited to environments where you explicitly intend that behavior.

The [quickstart](quickstart.md) reads credentials from environment variables to avoid storing
them in example code. See the generated `FMGSettings` reference for connection settings and
[advanced usage](advanced_usage.md#transport_retries_and_timeouts) for timeout and retry behavior.

## Install from source

To try the current repository version:

```shell
python -m pip install git+https://github.com/realvitya/pyfortinet.git
```

Source installations may differ from a published release. For editable installations, dependency
management with uv, and contribution checks, follow the [developer guide](../developer_guide/index.md).
