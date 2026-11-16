# Security profiles

Use an open connection from the [quickstart](../quickstart.md). Run the snippets on this page in order;
write examples require unused names and valid references in your selected ADOM. Await requests
when using an asynchronous client. See the [firewall overview](../firewall_objects.md) for
firmware coverage and shared conventions.

## ProfileGroup

`ProfileGroup` references existing security profiles by name. It does not create antivirus,
web-filter, or other profiles. Replace the profile names below with profiles present in your ADOM.

```python
from pyfortinet.fmg_api.firewall import ProfileGroup

profiles = ProfileGroup(
    name="example-security-profiles",
    av_profile="existing-antivirus",
    webfilter_profile="existing-webfilter",
    ips_sensor="existing-ips",
)
fmg.add(profiles)
```
