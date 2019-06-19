from unittest import TestCase, mock

import postal_admin_client


class PostalAdminTestcase(TestCase):
    client = None

    @classmethod
    def setUpClass(self):
        self.client = postal_admin_client.Client(
            'https://postal.test',
            email='me@somewhere',
            password='mypass',
        )
