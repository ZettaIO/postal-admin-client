import bs4
import logging
import requests

from postal_admin_client.httpclient import HTTPClient

logger = logging.getLogger(__name__)


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

    def create_organization(self, name: str, shortname: str = None):
        """
        Create an organization.
        Letting postal generate the shortname is generally safer.
        If supplying a shortname be sure it's not already in use.

        Args:
            name (str): Display name of the organization
        
        Keyword Args:
            shortname (str): used in usernames and the API to identify your organization.
                             It should only contain letters, numbers & hyphens. 
        """
        self._http.get('organizations/new')
        response = self._http.post(
            'organizations',
            data={
                'utf8': True,
                'organization[name]': name,
                'organization[permalink]': shortname,
                'commit': 'Create+organization',
            })

        # Construct the org info
        data = response.json()
        shortname = data['redirect_to'].split('/')[-1]
        return {'name': name, 'shortname': shortname}

    def list_organizations(self):
        """
        List all organization

        Returns:
            List of organization dicts
        """
        response = self._http.get()
        organizations = []

        soup = bs4.BeautifulSoup(response.content, features="html.parser")
        orgs = soup.find_all('a', {'class': 'largeList__link'})
        for org in orgs:
            organizations.append({
                'name': org.get_text().strip(),
                'shortname': org.get('href').split('/')[-1],
            })

        return organizations

    def delete_organization(self, shortname: str):
        """
        Delete an organization and all their resources

        Args:
            shortname (str): The organization to delete
        
        Raises:
            ValueError if password is incorrect
            HttpError is org does not exist
        """
        self._http.get('org/{}/delete'.format(shortname))
        response = self._http.post(
            path = 'org/{}/delete'.format(shortname),
            data={
                'utf8': True,
                '_method': 'delete',
                'return_to': '',
                'password': self._http._password,
                'commit': 'Delete+this+organization,+mail+servers+and+all+messages',
            },
        )
        data = response.json()
        # Success response: {"redirect_to":"/?nrd=1"}
        # Wrong pw response: {"alert":"The password you entered was invalid. Please check and try again."}
        if 'alert' in data:
            raise ValueError("Incorrect password entered when deleting organizaton")

    def user_list(self, shortname: str):
        pass

    def create_user(self, shortname: str, email: str, admin=False):
        """
        Create/invite a user in an organization.

        An email will be sent to the user with an invite.
        The first person invited to an organization will automatically be the owner.
        If the user already exist with the supplied email in postal
        they will get a simplified mail accepting an organization invite.
        If the user do not already have a user in postal a new user form is presented.

        Args:
            shortname (str): The organization
            email (str): New user email

        Keyword Args:
            admin (bool): Should the user be an administrator?
        """
        self._http.get('org/{}/users/new'.format(shortname))
        self._http.post(
            'org/{}/users'.format(shortname),
            data={
                'utf8': True,
                'invite': '',
                'organization_user[email_address]': email,
                'organization_user[admin]': admin,
                'commit': 'Add+User',
            },
        )
        # 422 when email is invalid
        # {"redirect_to":"https://postal.test/org/nada/users"}
