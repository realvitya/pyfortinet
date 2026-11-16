# pyfortinet

[//]: # (--8<-- [start:intro])

pyfortinet is a Python library for the FortiManager JSON-RPC API. Work with addresses, groups,
services, policies, and other supported resources as Python objects. The library handles session
authentication, request construction, and typed GET responses.

## Features

- High-level configuration models with Pydantic validation and API field aliases.
- Synchronous and asynchronous clients with consistent object operations.
- ADOM workspace locking and connection cleanup.
- Background task polling with progress callbacks.
- Dictionary requests and low-level clients for endpoints without a model.

Coverage is evolving. Check the code reference for available models and the target firmware's API
reference for supported fields. Direct FortiGate connections, token/SAML authentication, and
workflow session approval automation are not implemented.

[//]: # (--8<-- [end:intro])

## Installation

Python 3.9 or later is required.

```shell
python -m pip install pyfortinet
# Optional asynchronous support:
python -m pip install "pyfortinet[async]"
# Both asynchronous support and Rich output:
python -m pip install "pyfortinet[all]"
```

## Read firewall addresses

Set the example's environment variables for your FortiManager account and selected ADOM.
The account needs JSON-RPC API access. TLS certificate verification is enabled by default.

```python
import os

from pyfortinet import FMG
from pyfortinet.fmg_api.common import F
from pyfortinet.fmg_api.firewall import Address

config = {
    "base_url": os.environ["FMG_URL"],
    "username": os.environ["FMG_USERNAME"],
    "password": os.environ["FMG_PASSWORD"],
    "adom": os.environ["FMG_ADOM"],
}

with FMG(**config) as fmg:
    for address in fmg.get(Address, F(name__like="server%")).data:
        print(address.name, address.subnet)
```

Use `async with FMG(**config) as fmg:` and `await fmg.get(...)` for asynchronous code.
`AsyncFMG` is also available directly.

## Documentation

- [Quickstart](https://realvitya.github.io/pyfortinet/user_guide/quickstart/):
  connect, read objects, and make a targeted update.
- [API concepts](https://realvitya.github.io/pyfortinet/user_guide/api_concepts/):
  move from JSON-RPC operations to high-level Python objects.
- [How-tos](https://realvitya.github.io/pyfortinet/user_guide/howto/):
  filtering, object lifecycle, groups, mappings, workspace locks, and installation tasks.
- [Developer guide](https://realvitya.github.io/pyfortinet/developer_guide/):
  setup, implementing models, testing, and documentation maintenance.

If you use [How to FortiManager API](https://how-to-fortimanager-api.readthedocs.io/en/latest/),
start with the API concepts page. That guide provides broad API context; pyfortinet's user guide
shows workflows using the models implemented by this library.
