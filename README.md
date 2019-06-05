
# postal-admin-client

Admin client for the open source mail delivery platform
[postal](https://github.com/atech/postal).

This package is only for postal administrators
and do not include support for the message and send API.

Postal currently don't have a proper HTTP API for administation
so we rely on faking a browers filling forms and dealing with
csfr tokens to make rails happy.

This can for example be used to manage and create new organizations.
