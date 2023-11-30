# Fortinet Python library

This project implement easy way of handling Fortinet device management from Python.

## Quick example

### FMG

```python
"""Simple example"""
from pyfortinet import FMG
config = {
    "base_url": "https://myfmg.com",
    "username": "myuser",
    "password": "verysecret",
    "adom": "root",
    "verify": False
}
with FMG(**config) as fmg:
    ver = fmg.get_version()
```

## Installation

TBD

## Setup

TBD
