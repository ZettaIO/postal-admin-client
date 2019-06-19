from requests.exceptions import HTTPError

from base import PostalAdminTestcase
from utils import fixtures


class OrganizationTests(PostalAdminTestcase):

    def test_list(self):
        """List organization"""
        with fixtures():
            orgs = self.client.list_organizations()
            self.assertEqual(orgs, self.orgs)

    def test_create(self):
        """Create an organization"""
        json = {"redirect_to": "/org/il"}
        with fixtures('POST', '/organizations', json=json):
            org = self.client.create_organization('Illuminati')
            self.assertEqual(org, {'name': 'Illuminati', 'shortname': 'il'})

    def test_create_existing(self):
        """Esure 422 error is picked up when shortname is taken"""
        json = {"error": "Shortname already taken"}
        with fixtures('POST', '/organizations', json=json, status_code=422):
            with self.assertRaises(HTTPError):
                org = self.client.create_organization('Illuminati', shortname='il')
