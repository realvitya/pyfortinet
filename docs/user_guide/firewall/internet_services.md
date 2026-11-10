# Internet services

Use an open connection from the [quickstart](../quickstart.md). Run the snippets on this page in order;
write examples require unused names and valid references in your selected ADOM. Await requests
when using an asynchronous client. See the [firewall overview](../firewall_objects.md) for
firmware coverage and shared conventions.

## InternetService

`InternetService` models the Internet Service Database fields on `firewall/internet-service`.
The supplied reference exposes only GET, SET, and UPDATE at the collection URL. It defines no
ADD, DELETE, CLONE, item-by-ID URL, or dynamic mapping. Unsupported object operations raise
`FMGWrongRequestException` before sending a request.

```python
from pyfortinet.fmg_api.firewall import InternetService

service = fmg.get(InternetService(id=65536)).first()  # id becomes a GET filter
```

An ID remains in SET/UPDATE data; it is not appended to the URL. Firmware decides which
database attributes are editable; the reference does not mark individual fields read-only.
