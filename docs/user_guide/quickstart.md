# Quick Start Guide

## Installation

In most cases installation via pip is the simplest and best way to install pyfortinet.
See [here](installation.md) for advanced installation details.

```shell
pip install pyfortinet
```

## A Simple Example (get object)

```python
from pyfortinet import FMGBase
from pyfortinet.fmg_api.firewall import Address

settings = {
    "base_url": "https://myfmg.co.com",
    "verify": False,
    "username": "admin",
    "password": "verysecret",
    "adom": "root"
}
with FMGBase(**settings) as conn:
    search = Address(name="test-obj")
    result = conn.get(search)
```
