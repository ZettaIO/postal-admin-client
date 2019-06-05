from urllib.parse import urljoin

import bs4
import requests


class HTTPClient:
    """
    Hides some of the hacky magic from the actual client
    """
    def __init__(self, base_url: str, email: str = None, password: str = None):
        self._base_url = base_url
        self._sess = requests.Session()
        self._email = email
        self._password = password
        self._is_authenticated =  False
        self._authenticity_token = None

    def post(self, path=None, data=None, auth=True) -> requests.Response:
        return self.request('POST', path=path, data=data, auth=auth)

    def get(self, path=None, params=None, auth=True) -> requests.Response:
        return self.request('GET', path=params, params=params, auth=auth)

    def request(self, method: str, path: str = None, data: dict = None,
            params: dict = None, auth: bool = True) -> requests.Response:
        """
        Generic http request handling csrf

        Args:
            method (str): The http method
            path (str): Relative path
            data (dict): Dictonary of data
            params (dict): Query parameters
            auth (bool): Authenticate if needed
        
        Returns:
            HttpResponse
        """
        # We cannot do a post request before an initial request
        # have been done to obtain an authenticity token
        if not self._is_authenticated and auth is True:
            self.get(auth=False)
            self._authenticate()

        if method == 'POST' and not self._authenticity_token:
            self.get()

        if path:
            url = urljoin(self._base_url, path)            
        else:
            url = self._base_url

        print(method, url)

        response = self._sess.request(
            method,
            url,
            data=data,
            params=params
        )
        response.raise_for_status()
        self._authenticity_token = self._find_authenticity_token(response)
        return response

    def _find_authenticity_token(self, response) -> str:
        """
        Find the authenticity_token/crsf token.
        we need this in the next request in case we are POSTing
        """
        soup = bs4.BeautifulSoup(response.content, features="html.parser")
        metas = soup.find_all('meta')
        authenticity_token = None
        for meta in metas:
            if meta.get('name') == 'csrf-token':
                token = meta.get('content')
                if token:
                    return token

        raise ValueError('Cannot parse out authenticity_token')

    def _authenticate(self):
        """Quck and dirty auth"""
        result = self.request(
            'POST',
            'login',
            params={
                'authenticity_token': self._authenticity_token,
                'email_address': self._email,
                'password': self._password,
            },
            auth=False,
        )
        self._is_authenticated = True
