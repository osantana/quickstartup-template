# coding: utf-8


from django.core.urlresolvers import NoReverseMatch

from ..tests.base import BaseTestCase, TEST_ROOT_DIR
from .models import Page
from .urlresolver import page_reverse


TEMPLATE_DIRS = (
    str(TEST_ROOT_DIR / "templates"),
)


class PageTest(BaseTestCase):
    def test_success_reverse(self):
        Page.objects.create(slug="about", template="about.html")
        url = page_reverse("about")
        self.assertEquals("/about/", url)

    def test_fail_reverse_missing_template(self):
        with self.assertRaises(NoReverseMatch):
            page_reverse("unknown")

    def test_fail_reverse_invalid_url(self):
        self.assertRaises(NoReverseMatch, page_reverse, "/")

    def test_bootstrap_pages(self):
        self.assertEquals(Page.objects.get(slug="").get_absolute_url(), "/")
        self.assertEquals(Page.objects.get(slug="terms").get_absolute_url(), "/terms/")
        self.assertEquals(Page.objects.get(slug="privacy").get_absolute_url(), "/privacy/")

    def test_filter_invalid_pages(self):
        pages = Page.objects.all()
        self.assertNotIn("inv@lid", pages)

    def test_success_terms_page_access(self):
        response = self.client.get("/terms/")
        self.assertContains(response, "<title>Terms of Service —")

    def test_success_terms_page_access_missing_trailing_slash(self):
        response = self.client.get("/terms")
        self.assertContains(response, "<title>Terms of Service — ")

    def test_success_privacy_page_access(self):
        response = self.client.get("/privacy/")
        self.assertContains(response, "<title>Privacy Policy —")

    def test_fail_page_404(self):
        response = self.client.get("/unknown/")
        self.assertStatusCode(response, 404)

    def test_fail_invalid_url(self):
        response = self.client.get("/err/or/")
        self.assertStatusCode(response, 404)

    def test_call_template_with_error_and_debug_disabled(self):
        Page.objects.create(slug="buggy-template", template="buggy-template.html")
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS, DEBUG=False):
            url = page_reverse("buggy-template")
            response = self.client.get(url)
        self.assertStatusCode(response, 404)  # original error is 404 because we dont map pages urls

    def test_reraise_when_calling_template_with_error_and_debug_enabled(self):
        Page.objects.create(slug="buggy-template", template="buggy-template.html")
        with self.settings(TEMPLATE_DIRS=TEMPLATE_DIRS, DEBUG=True):
            url = page_reverse("buggy-template")
            with self.assertRaises(NoReverseMatch):
                self.client.get(url)

    def test_index_page_anonymous_user(self):
        response = self.client.get("/")
        self.assertStatusCode(response, 200)
        self.assertTemplateUsed(response, "website/index.html")
        self.assertInHTML("<title>Django Quickstartup</title>", response.content.decode("utf-8"))
