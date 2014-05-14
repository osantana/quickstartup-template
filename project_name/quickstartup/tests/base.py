# coding: utf-8


from pathlib import Path

from django.test import TestCase

from quickstartup.website.urlresolver import flush_pages_cache


TEST_ROOT_DIR = Path(__file__).parent


class BaseTestCase(TestCase):
    def setUp(self):
        flush_pages_cache()

    def assertStatusCode(self, response, code):
        self.assertEquals(response.status_code, code, str(response.content))
