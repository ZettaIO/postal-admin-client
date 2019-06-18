from unittest import TestCase
from postal_admin_client import utils


class UtilsTests(TestCase):

    def test_find_all_urls(self):
        """Find a single url in javascript snippet"""
        data = """
        Turbolinks.clearCache()
        Turbolinks.visit("https://postal.test/org/il", {"action":"replace"})
        """
        urls = utils.find_all_urls(data)
        self.assertEqual(len(urls), 1)
        self.assertAlmostEqual(urls[0], 'https://postal.test/org/il')

    def test_find_all_urls_multiple(self):
        """Find multiple urls in a string"""
        urls = [
            'https://postal.test/org/il',
            'https://postal.test/org/os',
            'https://postal.test/org/an',
            'https://postal.test/org/bi',
        ]
        data = "\n".join(urls)
        result = utils.find_all_urls(data)
        self.assertEqual(result, urls)
