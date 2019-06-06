
# postal-admin-client

**WORK IN PROGRESS: This package is still under development
and currenly do not have any releases.**

Admin client for the open source mail delivery platform
[postal](https://github.com/atech/postal).

This package is only for postal administrators
and do not include support for the message and send API.

Postal currently don't have a proper HTTP API for administation
so we rely on faking a brower filling forms and dealing with
csrf tokens to make rails happy.

This can for example be used to manage and create new organizations.

## Example

```python
from pprint import pprint
import postal_admin_client

client = postal_admin_client.Client(
    'https://postal.example.com',
    email='user@example.com',
    password='myhopefullysecurepassword',
)

orgs = client.list_organizations()
pprint(orgs, indent=2)
```

## Logging

This package is using `logging`. You can configure logging behaviour
(handler, log level, propagation etc) by obtaining the logger for this package.

```python
logger = logging.getLogger('postal_admin_client')
```
