
# postal-admin-client

Admin client for the open source mail delivery platform
[postal](https://github.com/atech/postal).

This package is only for postal administrators
and do not include support for the message and send API.

Postal currently don't have a proper HTTP API for administation
so we rely on faking a browers filling forms and dealing with
csfr tokens to make rails happy.

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
