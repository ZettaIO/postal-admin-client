import bs4
import requests

from postal_admin_client.httpclient import HTTPClient


class Client:

    def __init__(self, base_url: str, email: str = None, password: str = None):
        """
        Create an admin client and session

        Args:
            base_url (str): URL to your postal web page
            email (str): Email to authenticate with
            password (str): Password
        """
        self._http = HTTPClient(base_url, email=email, password=password)

    def create_organization(self, name: str, shortname: str):
        """
        Create an organization

        Args:
            name (str): Display name of the organization
            shortname (str): used in usernames and the API to identify your organization.
                             It should only contain letters, numbers & hyphens. 
        """
        self._http.get('organizations/new')
        response = self._http.post(
            'organizations',
            params={
                'utf8': True,
                'organization[name]': name,
                'organization[permalink]': shortname,
                'commit': 'Create+organization',
            })
        # TODO: Parse result

    def list_organizations(self):
        response = self._http.get()
        organizations = []

        soup = bs4.BeautifulSoup(open('list_org.html', mode='r'), features="html.parser")
        orgs = soup.find_all('a', {'class': 'largeList__link'})
        for org in orgs:
            organizations.append({
                'name': org.get_text().strip(),
                'shortname': org.get('href').split('/')[-1],
            })

        return organizations
