# Quickstart

Use `FMG` to work with FortiManager objects in Python. This example reads firewall addresses;
it does not change configuration. Python 3.9 or later is required.

## Install and configure

```shell
python -m pip install pyfortinet
```

Use a FortiManager account with JSON-RPC API access and permission to read the selected ADOM.
Set `FMG_URL`, `FMG_USERNAME`, `FMG_PASSWORD`, and `FMG_ADOM` in your environment before running
the example. These are example-specific variable names read explicitly by the code below.

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
    addresses = fmg.get(Address, F(name__like="server%"))
    for address in addresses.data:
        print(address.name, address.subnet)

    server = fmg.get(Address(name="server1")).first()
    if server is None:
        print("server1 was not found")
    else:
        print(server.name, server.subnet)
```

The context opens an authenticated session and closes it on exit. High-level GET responses
contain typed models in `.data`. `.first()` returns an object or `None` when nothing matches.
Request failures raise exceptions by default. TLS certificate verification is enabled by default.

## Update an address

The following example uses the same `config` and changes an existing address in the selected ADOM:

```python
with FMG(**config) as fmg:
    server = fmg.get(Address(name="server1")).first()
    if server is None:
        raise LookupError("Create server1 before running this example")
    fmg.update(Address(name=server.name, subnet="192.0.2.0/24"))
```

A model containing only the fields to change avoids writing unrelated values from a previous GET.
Fetched objects are also bound to their client, so `server.update()` is available after changing
their fields. Keep object operations inside the connection context.

On normal exit, the client attempts to commit workspaces it has locked. This saves changes in
FortiManager; installing configuration onto a FortiGate is a separate operation. Workspace
discard is not a general rollback mechanism. See the [how-tos](howto.md).

## Use the same API asynchronously

Install `pyfortinet[async]`, then use the same imports and `config` with an asynchronous context:

```python
import asyncio


async def main():
    async with FMG(**config) as fmg:
        addresses = await fmg.get(Address)
        for address in addresses.data:
            print(address.name, address.subnet)


asyncio.run(main())
```

`async with FMG(...)` yields an `AsyncFMG` client. Await its requests and operations on bound
objects. `get_obj(...)` only constructs or binds a local model and is not awaited. You can also
import `AsyncFMG` directly for explicit asynchronous connection management.

Continue with [API concepts](api_concepts.md) and the [task-oriented how-tos](howto.md).
