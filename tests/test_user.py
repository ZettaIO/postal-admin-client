from requests.exceptions import HTTPError

from base import PostalAdminTestcase
from utils import fixtures


class UserTests(PostalAdminTestcase):

    def test_create(self):
        """List organization"""
        json = {"redirect_to":"https://postal.test/org/il/users"}
        with fixtures('POST', '/org/il/users', json=json):
            orgs = self.client.create_user('il', 'user@illuminati.test', admin=True)
