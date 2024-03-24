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
