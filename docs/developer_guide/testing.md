# Test guide

## Testing config file

It is advisable to put all lab related configs and files to a separate folder which is not part of the GIT repository.
I used to use private folder which is excepted from GIT. In that folder you can store your config files. One of the most
important config file is `lab-config.yml`. This file contains access to your lab environment.

Example of `lab-config.yml` file:

```yaml
---
fmg:
  base_url: https://myfmg.co.com/
  verify: false
  username: admin
  password: verysecret
  adom: root
```

## Offline regression tests

Run `uv run pytest tests/unit` (or `pytest tests/unit` in an activated environment) to check shared sync
and async behavior without a lab configuration or network access.
These tests mock the transport and exercise the public client methods.

## Local transport checks

Run `uv run pytest tests/transport` to verify native HTTP timeouts against a temporary loopback-only TCP peer.
These tests need permission to create local sockets and do not connect to a FortiManager device.
