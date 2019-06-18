from unittest import TestCase, mock
from base import PostalAdminTestcase
from utils import fixture_response

REQUEST_FUNC = 'requests.sessions.Session.request'


class OrganizationTests(PostalAdminTestcase):

    def test_list(self):
        """List organization"""
        with mock.patch(REQUEST_FUNC, new=fixture_response('org_list.html')):
            orgs = self.client.list_organizations()
            self.assertEqual(orgs, self.orgs)
