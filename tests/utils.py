import json as js
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

from requests.exceptions import HTTPError

FIXTURE_DIR = Path(__file__).parent / 'fixtures'

# path: file
FIXTURES = {
    'GET:': {'file': 'org_list.html'},
    'GET:/login': {'file': 'login.html'},
    'POST:/login': {'file': 'org_list.html'},
    'GET:/organizations/new': {'file': 'org_new.html'}
}


@lru_cache(maxsize=None)
def load_fixture(name: str):
    with open(FIXTURE_DIR / name, mode='rb') as fd:
        return fd.read()


def get_fixture(path):
    entry = FIXTURES.get(path)
    if entry is not None:
        if 'file' in entry:
            return load_fixture(entry['file'])
        if 'content' in entry:
            return entry['content']
        if 'json' in entry:
            return js.dumps(entry['json'])

    raise ValueError("No fixture found for path {}".format(path))


def fixture_response(override_method=None, override_path=None, fixture=None, json=None, status_code=200):
    """Creates a fake request method returning an http response with a specific response"""
    if fixture:
        override_content = load_fixture(fixture)

    if json:
        override_content = js.dumps(json).encode()

    def request(sess, method, url, *args, **kwargs):
        path = urlparse(url).path
        fixture_key = "{}:{}".format(method, path)
        print("session", method, path)

        if path == override_path and method == override_method:
            content = override_content
        else:
            content = get_fixture(fixture_key)

        return FakeHttpResponse(
            status_code=status_code,
            url=url,
            content=content,
        )
    return request


class FakeHttpResponse:
    encoding = 'utf-8'

    def __init__(self, url=None, content=None, status_code=200):
        self._content = content
        self._status_code = status_code
        self._url = url

    @property
    def status_code(self):
        return self._status_code

    @property
    def url(self):
        return self._url

    @property
    def content(self) -> bytes:
        return self._content

    def json(self):
        return js.loads(self._content)

    def raise_for_status(self):
        if self._status_code > 400:
            raise HTTPError(self._status_code)
