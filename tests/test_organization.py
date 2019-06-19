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
        """Ensure 422 error is picked up when shortname is taken"""
        json = {"error": "Shortname already taken"}
        with fixtures('POST', '/organizations', json=json, status_code=422):
            with self.assertRaises(HTTPError):
                org = self.client.create_organization('Illuminati', shortname='il')

    def test_delete(self):
        """Test a simple delete"""
        json = {"redirect_to":"/?nrd=1"}
        with fixtures('POST', '/org/nada/delete', json=json):
            self.client.delete_organization('nada')

    def test_delete_wrong_pw(self):
        """Response when password is wrong"""
        json = {"alert":"The password you entered was invalid. Please check and try again."}
        with fixtures('POST', '/org/nada/delete', json=json):
            with self.assertRaises(ValueError):
                self.client.delete_organization('nada')

    def test_delete_nonexistent(self):
        """Ensure trying to delete a non-existent forwards 404"""
        json = {"status":404,"error":"Not Found"}
        with fixtures('POST', '/org/nada/delete', json=json, status_code=404):
            with self.assertRaises(HTTPError):
                self.client.delete_organization('nada')
