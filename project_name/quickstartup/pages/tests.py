# coding: utf-8


from django.core.urlresolvers import NoReverseMatch

from ..tests.base import BaseTestCase, TEST_ROOT_DIR
from quickstartup.pages.urlresolver import page_reverse, list_pages


TEMPLATE_DIRS = (
    str(TEST_ROOT_DIR / "templates"),
)


class PageTest(BaseTestCase):
    def test_success_reverse(self):
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS):
            url = page_reverse("about")

        self.assertEquals("/about/", url)

    def test_fail_reverse_missing_template(self):
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS):
            self.assertRaises(NoReverseMatch, page_reverse, "unknown")

    def test_fail_reverse_invalid_url(self):
        self.assertRaises(NoReverseMatch, page_reverse, "/")

    def test_list_pages(self):
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS):
            pages = list_pages()

        self.assertIn("about", pages)
        self.assertIn("terms", pages)

    def test_filter_invalid_pages(self):
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS):
            pages = list_pages()

        self.assertNotIn("inv@lid", pages)

    def test_success_page_access(self):
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS):
            response = self.client.get("/about/")

        self.assertContains(response, "<title>About</title>")

    def test_success_page_access_missing_trailing_slash(self):
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS):
            response = self.client.get("/about")

        self.assertContains(response, "<title>About</title>")

    def test_fail_page_404(self):
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS):
            response = self.client.get("/unknown/")

        self.assertEquals(response.status_code, 404)

    def test_fail_invalid_url(self):
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS):
            response = self.client.get("/err/or/")

        self.assertEquals(response.status_code, 404)
