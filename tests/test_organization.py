from unittest import TestCase, mock
from base import PostalAdminTestcase
from utils import fixture_response

REQUEST_FUNC = 'requests.sessions.Session.request'


class OrganizationTests(PostalAdminTestcase):

    def test_list(self):
        """List organization"""
        with mock.patch(REQUEST_FUNC, new=fixture_response()):
            orgs = self.client.list_organizations()
            self.assertEqual(orgs, self.orgs)

    def test_create(self):
        """Create an organization"""
        json = {"redirect_to": "/org/il"}
        with mock.patch(REQUEST_FUNC, new=fixture_response('POST', '/organizations', json=json)):
            org = self.client.create_organization('Illuminati')
            self.assertEqual(org, {'name': 'Illuminati', 'shortname': 'il'})
