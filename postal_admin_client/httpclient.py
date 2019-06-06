from urllib.parse import urljoin
import logging

import bs4
import requests

logger = logging.getLogger(__name__)


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

    def post(self, path=None, data=None, json=None, params=None, auth=True) -> requests.Response:
        return self.request('POST', path=path, data=data, json=None, params=params, auth=auth)

    def get(self, path=None, params=None, auth=True) -> requests.Response:
        return self.request('GET', path=path, params=params, auth=auth)

    def request(self, method: str, path: str = None, data: dict = None,
            json: dict = None, params: dict = None, auth: bool = True) -> requests.Response:
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
        if not self._is_authenticated:
            self._authenticate()

        url = self._url(path)
        headers = {}
        if method == 'POST':
            headers={
                'X-CSRF-Token': self._authenticity_token,
                # 'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'credentials': 'same-origin',
            }

        logger.info('HTTP %s %s', method, url)
        logger.debug('Headers: %s', headers)
        logger.debug('Data: %s', data)
        logger.debug('Json: %s', json)
        logger.debug('Params: %s', params)

        response = self._sess.request(
            method,
            url,
            data=data,
            json=json,
            params=params,
            headers=headers,
        )
        logger.debug("Status code %s", response.status_code)
        logger.debug("Respons body:\n %s", response.content.decode())
        try:
            response.raise_for_status()
        except Exception as ex:
            logger.error(ex)
            raise

        if method == 'GET':
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

        logger.debug('authenticity_token %s', authenticity_token)
        return authenticity_token

    def _authenticate(self):
        """
        Obtain and post the login form.
        This process needs the authenticity token in the post body itself
        and do not use X-CSRF-Token header like posts in logged in state.
        """
        response = self._sess.get(self._url('login'))
        self._authenticity_token = self._find_authenticity_token(response)
        response = self._sess.post(
            self._url('login'),
            params={
                'utf8': True,
                'authenticity_token': self._authenticity_token,
                'email_address': self._email,
                'password': self._password,
            },
        )
        self.authenticity_token = self._find_authenticity_token(response)
        self._is_authenticated = True

    def _url(self, path):
        if path:
            return urljoin(self._base_url, path)            

        return self._base_url
