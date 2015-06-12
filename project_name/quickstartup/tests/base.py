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
        self.assertEquals(response.status_code, code,
                          "{} != {}\n{}".format(response.status_code, code, response.content))

    def get_mail_payloads(self, message):
        text = ""
        html = ""

        for payload in message.message().get_payload():
            if payload.get_content_type() == "text/plain":
                text = payload.as_string()
            if payload.get_content_type() == "text/html":
                html = payload.as_string()

        return text, html
