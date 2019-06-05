from urllib.parse import urljoin
import logging

import bs4
import requests

logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


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

    def post(self, path=None, data=None, params=None, auth=True) -> requests.Response:
        return self.request('POST', path=path, data=data, params=params, auth=auth)

    def get(self, path=None, params=None, auth=True) -> requests.Response:
        return self.request('GET', path=path, params=params, auth=auth)

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
            self._authenticate()

        if method == 'POST' and not self._authenticity_token:
            logger.info('Attempting post without authenticity token. Doing additional get request')
            self.get(path=path, auth=False)

        if path:
            url = urljoin(self._base_url, path)            
        else:
            url = self._base_url

        logger.info('HTTP %s %s', method, url)

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
                authenticity_token = meta.get('content')
                break

        if not authenticity_token:
            raise ValueError('Cannot parse out authenticity_token')

        logger.info('authenticity_token %s', authenticity_token)
        return authenticity_token

    def _authenticate(self):
        """Quck and dirty auth"""
        self.get('login', auth=False)
        result = self.post(
            path='login',
            params={
                'utf8': True,
                'authenticity_token': self._authenticity_token,
                'email_address': self._email,
                'password': self._password,
            },
            auth=False,
        )
        self._is_authenticated = True
