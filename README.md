
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
>> import postal_admin_client
>>
>> client = postal_admin_client.Client(
>>     'https://postal.example.com',
>>     email='user@example.com',
>>     password='myhopefullysecurepassword',
>> )
>>
>> client.list_organizations()
[{'name': 'Anansi Technologies', 'shortname': 'at'},
 {'name': 'Council of Venice', 'shortname': 'cov'},
 {'name': 'Orochi Group', 'shortname': 'og'}]
>> client.create_organization('Illuminati')
{'name': 'Illuminati', 'shortname': 'il'}
```

## Supported Operations

* List organizations
* Create organization
* Delete organization
* List users in organization
* Invite user to organization

## Improvements

* Properly parse out validation errors. For example: `create_user`
  raises `HTTPError(422)` in three different cases and it would be useful
  for the user to easily be able to separate between them.

## Logging

This package is using `logging`. You can configure logging behaviour
(handler, log level, propagation etc) by obtaining the logger for this package.

```python
logger = logging.getLogger('postal_admin_client')
```

## Contributing

Do not hesistate creating pull requests with completed or
partial work or create issues. There very likely many
things to improve.
