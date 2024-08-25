# Fortinet Python library

[//]: # (--8<-- [start:intro])

This project is a Python library for Fortinet products' REST API. Currently, only Fortimanager is supported, but
extensions for various products are planned. Current state is rather a Proof of Concept.

## Features

* FMG API
    * Low level API access via passing dict to various calls (add, get, set, update, exec)
    * Automatic login (Currently, only user/password authentication is supported)
    * Automatic locking in workspace mode (Currently, only ADOM locking is supported)
    * High level API using all kind of objects (see some examples below)
        * Only couple of objects are supported yet (being POC project), but extension is planned for most used functions!
        * Task handling with waiting and callback function (to support progress bar, logging, etc.)
    * Async code is supported

### Planned features

* FMG API
    * Extended authentication capabilities (token, SAML)
    * Extended locking capabilities to support object and package level locking and fallback feature to ADOM locking
    * Proxy FortiOS API calls using objects of FortiOS API
* FortiOS API
    * Similar capabilities to FMG API

[//]: # (--8<-- [end:intro])

## Quick examples

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
    # create and assign new address object to FMG
    server1 = fmg.get_obj(Address(name="server1", subnet="192.168.0.1/32"))
    server1.add()
    # get exact address object from FMG
    server2 = fmg.get(Address(name="server2")).first()
    print(server2.name)
    # get list of address object from FMG
    servers = fmg.get(Address, F(name__like="server%"))
    print(servers.data)

    # Low level call is also supported in case object was not available
    address_request = {
        "url": "/pm/config/adom/root/obj/firewall/address",
        "filter": [["name", "==", "test-address"]],
    }
    result = fmg.get(address_request)
    print(result.data["data"])
```

### AsyncFMG

Async code is also supported via `AsyncFMG`. Intention is to support async frameworks like
[FastAPI](https://fastapi.tiangolo.com/).

```python
import asyncio
from pyfortinet import AsyncFMG
from pyfortinet.fmg_api.firewall import Address
from pyfortinet.fmg_api.common import F

async def main():
    config = {
        "base_url": "https://myfmg.com",
        "username": "myuser",
        "password": "verysecret",
        "adom": "root",
        "verify": False
    }
    async with AsyncFMG(**config) as fmg:
        # create and assign new address object to FMG
        server1 = fmg.get_obj(Address(name="server1", subnet="192.168.0.1/32"))
        await server1.add()
        # get list of addresses from FMG and pick the first element
        address = (await fmg.get(Address, F(name__like="test-firewall-addr%"))).first()
        # update address object
        address.subnet = "10.0.1.0/24"
        result = await address.update()

asyncio.run(main())
```

### FMGBase

``FMGBase`` is a lower level API class which implements base functions. Purpose is to serve the inherited higher level
classes like ``FMG``.

```python
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
    result = fmg.get(address_request)
    print(result.data["data"])
```

### Extending FMG capabilities

It is possible to extend FMG capabilities by inheriting from this FMG class and adding custom methods to it.
Please check [Fortimanager Template Sync](https://github.com/realvitya/fortimanager-template-sync) project for an
example of how to do it!

## Installation

The library can be installed via PIP from [PyPi](https://pypi.org/project/pyfortinet).

```shell
# basic install
pip install pyfortinet

# install with async dependency
pip isntall pyfortinet[async]

# enable rich traceback
pip install pyfortinet[rich]

# simple install with all feature dependency
pip install pyfortinet[all]
```
