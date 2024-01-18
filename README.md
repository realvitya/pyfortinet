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
```

## Installation

TBD

## Setup

TBD
