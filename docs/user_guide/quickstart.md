# Quick Start Guide

## Installation

In most cases installation via pip is the simplest and best way to install pyfortinet.
See [here](installation.md) for advanced installation details.

```shell
pip install pyfortinet
```

## A Simple Example (get object)

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
    # get exact address object from FMG
    server2 = fmg.get(Address, F(name="server2")).first()
    print(server2.name)
```

## Updating existing object

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
    # get exact address object from FMG
    server = fmg.get(Address, F(name="server1")).first()
    server.subnet = "10.1.1.1/24"
    server.update()
```

## Filtering

`F` filter function can be used to compile complex search filters. More examples can be found in the respective testing
functions:

??? example "F filter examples"

    ```python
    --8<-- "tests/fmg/test_common.py"
    ```

```python title="Short examples"
from pyfortinet import FMG
from pyfortinet.fmg_api.firewall import Address
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.common import F

config = {
    "base_url": "https://myfmg.com",
    "username": "myuser",
    "password": "verysecret",
    "adom": "root",
    "verify": False
}
with FMG(**config) as fmg:
    # simple 'or'
    server1_and_2 = fmg.get(Address, F(name="server1") + F(name="server2")).data
    # list devices with name dc-fw-* which connection status is not up
    firewalls = fmg.get(Device, F(name__like="dc-fw-%") & ~F(conn_status="up")).data
```

## Task run

Exec objects are called Tasks. These have extra functionality like waiting. This is an example of running device
settings installation on devices with modified config status:

```python
from pyfortinet import FMG
from pyfortinet.fmg_api.common import Scope
from pyfortinet.fmg_api.dvmdb import Device
from pyfortinet.fmg_api.common import F

config = {
    "base_url": "https://myfmg.com",
    "username": "myuser",
    "password": "verysecret",
    "adom": "root",
    "verify": False
}
with FMG(**config) as fmg:
    devices: List[Device] = fmg.get(Device, conf_status="mod").data
    # for simplicity, assume all device is single mode
    task: InstallDeviceTask = fmg.get_obj(
        InstallDeviceTask, adom=fmg.adom, scope=[Scope(name=test_device.name, vdom="root")], flags=["auto_lock_ws"]
    )
    result: FMGResponse = task.exec()
    # block here until task is done. Print task percentage and log in the meanwhile
    result.wait_for_task(callback=lambda percent, log: print(f"Task at {percent}%: {log}"))
```
