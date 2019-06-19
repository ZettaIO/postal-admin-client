[![pypi](https://badge.fury.io/py/postal-admin-client.svg)](https://pypi.python.org/pypi/demosys-py) [![travis](https://api.travis-ci.org/ZettaIO/postal-admin-client.svg?branch=master)](https://travis-ci.org/ZettaIO/postal-admin-client)

# postal-admin-client

A python 3.5+ admin client for the open source mail delivery platform
[postal](https://github.com/atech/postal).

This package is only for postal administrators
and do not include support for the message and send API.

Postal currently don't have a proper HTTP API for administation
so we rely on faking a brower filling forms and dealing with
csrf tokens to make rails happy.

This can for example be used to manage and create new organizations.

This package can be installed from PyPI

```bash
pip install postal-admin-client
```

## Example

Initalize client

```python
>> import postal_admin_client
>>
>> client = postal_admin_client.Client(
>>     'https://postal.example.com',
>>     email='user@example.com',
>>     password='myhopefullysecurepassword',
>> )
```

List/create/delete organization

```python
>> client.list_organizations()
[{'name': 'Anansi Technologies', 'shortname': 'at'},
 {'name': 'Council of Venice', 'shortname': 'cov'},
 {'name': 'Orochi Group', 'shortname': 'og'}]
>> client.create_organization('Illuminati')
{'name': 'Illuminati', 'shortname': 'il'}
>> client.delete_organization('li')
```

List and create/invite users

```python
>> client.list_users()
[{'name': 'Kirsten Geary', 'email': 'kirsten.geary@illuminati.test'},
 {'name': 'Alex McCall', 'email': 'alex.mccall@illuminati.test'}]
>> client.create_user('il', 'nadia.shestova@illuminati.test', admin=False)
```

## Supported Operations

* List organizations
* Create organization
* Delete organization
* List users in organization
* Invite user to organization

## Dev Setup

Basic Setup

```bash
python -m virtualenv .venv
. .venv/bin/activate
python setup.py develop
```

Tests

```bash
pip install -r tests/requirements.txt
tox
```

## Improvements

* Properly parse out validation errors. For example: `create_user`
  raises `HTTPError(422)` in three different cases and it would be useful
  for the user to easily be able to separate between them.
* Add CLI support
* Support more operations

## Logging

This package is using `logging`. You can configure logging behaviour
(handler, log level, propagation etc) by obtaining the logger for this package.

```python
logger = logging.getLogger('postal_admin_client')
```

## Contributing

Do not hesistate creating pull requests with completed or
partial work or create issues. There are very likely many
things to improve.
