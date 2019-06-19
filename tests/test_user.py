from requests.exceptions import HTTPError

from base import PostalAdminTestcase
from utils import fixtures


class UserTests(PostalAdminTestcase):
    users = [
        {'name': 'Kirsten Geary', 'email': 'kirsten.geary@illuminati.test'},
        {'name': 'Alex McCall', 'email': 'alex.mccall@illuminati.test'},
    ]

    def test_list(self):
        with fixtures():
            users = self.client.list_users('il')
            self.assertEqual(users, self.users)

    def test_create(self):
        """Create/invite new user"""
        json = {"redirect_to":"https://postal.test/org/il/users"}
        with fixtures('POST', '/org/il/users', json=json):
            orgs = self.client.create_user('il', 'user@illuminati.test', admin=True)
