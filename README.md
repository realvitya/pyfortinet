# Fortinet Python library

This project implement easy way of handling Fortinet device management from Python.

## Quick example

### FMGBase

``FMGBase`` is a lower level API class which implements base functions. Purpose is to serve the inherited higher level
classes like ``FMG``.

```python
"""Simple example"""
from pyfortinet import FMGBase

config = {
    "base_url": "https://myfmg.com",
    "username": "myuser",
    "password": "verysecret",
    "adom": "root",
    "verify": False
}
with FMGBase(**config) as fmg:
    ver = fmg.get_version()
    print(ver)
    
    address_request = {
        "url": f"/pm/config/adom/root/obj/firewall/address",
        "filter": [["name", "==", "test-address"]],
    }
    result = fmg.get(request)
    print(result.data["data"])
```

### FMG

```python
from pyfortinet import FMG
from pyfortinet.fmg_api.firewall import Address
from pyfortinet.fmg_api.common import F

config = {
    "base_url": "https://myfmg.com",
    "username": "myuser",
    "password": "verysecret",
    "adom": "root",
    "verify": False
}
with FMG(**config) as fmg:
    server1 = fmg.get_obj(Address, name="server1", subnet="192.168.0.1/32")
    server1.add()
    
    server2 = fmg.get(Address, F(name="server2")).first()
    print(server2.name)
    
    servers = fmg.get(Address, F(name__like="server%"))
    print(servers.data)

```

### AsyncFMG

```python
import asyncio
from pyfortinet import AsyncFMG
from pyfortinet.fmg_api.firewall import Address
from pyfortinet.fmg_api.common import F

async def main():
    async with AsyncFMG(**config) as fmg:
        server1 = fmg.get_obj(Address, name="server1", subnet="192.168.0.1/32")
        await server1.add()

asyncio.run(main())
```

## Installation

The library can be installed via PIP from [PyPi](https://pypi.org/project/pyfortinet).

```shell
# basic install
pip install pyfortinet

# enable rich traceback
pip install pyfortinet[rich]
```
