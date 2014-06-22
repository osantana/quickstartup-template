# coding: utf-8


from pathlib import Path

from django.apps import apps
from django.test import TestCase

from quickstartup.website.bootstrap import bootstrap_website_pages


TEST_ROOT_DIR = Path(__file__).parent


class BaseTestCase(TestCase):
    def setUp(self):
        bootstrap_website_pages(apps)

    # noinspection PyPep8Naming
    def assertStatusCode(self, response, code):
        self.assertEquals(response.status_code, code, str(response.content))
