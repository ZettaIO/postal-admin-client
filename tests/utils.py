from pathlib import Path
from requests.exceptions import HTTPError

FIXTURE_DIR = Path(__file__).parent / 'fixtures'


def fixture_response(fixture, status_code=200):
    """Creates a fake request method returning an http response with a specific response"""
    with open(FIXTURE_DIR / fixture, mode='rb') as fd:
        content = fd.read()

    def request(*args, **kwargs):
        # content = open()
        return FakeHttpResponse(
            status_code=status_code,
            content=content,
        )
    return request


class FakeHttpResponse:
    encoding = 'utf-8'

    def __init__(self, content=None, status_code=200):
        self._content = content
        self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code

    @property
    def content(self) -> bytes:
        return self._content

    def raise_for_status(self):
        if self._status_code > 400:
            raise HTTPError(self._status_code)
