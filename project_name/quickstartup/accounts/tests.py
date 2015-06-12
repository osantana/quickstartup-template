# coding: utf-8

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.shortcuts import resolve_url
from django.test import override_settings, RequestFactory

from .templatetags.get_social_backends import get_social_backends
from .utils import get_social_message_errors
from ..tests.base import BaseTestCase

STATIC_ROOT = str(settings.FRONTEND_DIR / "static")


@override_settings(STATIC_ROOT=STATIC_ROOT)
class AccountTest(BaseTestCase):
    def setUp(self):
        super(AccountTest, self).setUp()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(email="test@example.com", password="secret")

    def test_simple_reset_password(self):
        url = reverse("qs_accounts:password_reset")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data)
        self.assertStatusCode(response, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertTemplateUsed(response, "mails/password-reset-subject.txt")
        self.assertTemplateUsed(response, "mails/password-reset.html")
        self.assertTemplateUsed(response, "mails/password-reset.txt")

        text, html = self.get_mail_payloads(mail.outbox[0])
        self.assertIn("Hi,", text)
        self.assertIn("<h3>Hi,</h3>", html)

        reset_token_url = response.context["path"]
        data = {"new_password1": "new-sekret", "new_password2": "new-sekret"}
        response = self.client.post(reset_token_url, data, follow=True)
        self.assertStatusCode(response, 200)
        self.assertContains(response, "Password reset complete")

        user = self.user_model.objects.get(email="test@example.com")  # reload user
        self.assertTrue(user.check_password("new-sekret"), "Password unchanged")

    def test_reset_password_with_passwords_that_does_not_match(self):
        url = reverse("qs_accounts:password_reset")
        data = {"email": "test@example.com"}
        response = self.client.post(url, data)

        reset_token_url = response.context["path"]

        data = {"new_password1": "sekret", "new_password2": "do-not-match"}
        response = self.client.post(reset_token_url, data)
        self.assertStatusCode(response, 200)
        self.assertContains(response, "The two password fields didn&#39;t match.")

    def test_simple_reset_password_of_user_with_name(self):
        self.user.name = "John Doe"
        self.user.save()

        url = reverse("qs_accounts:password_reset")
        data = {"email": "test@example.com"}
        self.client.post(url, data)

        text, html = self.get_mail_payloads(mail.outbox[0])
        self.assertIn("Hi John Doe,", text)
        self.assertIn("<h3>Hi John Doe,</h3>", html)

    def test_simple_signup(self):
        url = reverse("qs_accounts:signup")
        data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password1": "sekr3t",
            "password2": "sekr3t",
        }
        response = self.client.post(url, data)
        self.assertStatusCode(response, 302)

        user = self.user_model.objects.get(email="john.doe@example.com")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

        # TODO
        # self.assertEqual(user.activation_key_expired(), False)
        # message = mail.outbox[0]
        # self.assertIn("Hi John Doe,", message.html)
        # self.assertIn("<h3>Hi John Doe,</h3>", message.html)
        # TODO: continue from here
        # self.fail()
    # def test_redirect_if_authenticated(self):
    #     logged = self.client.login(username=self.user.email, password='secret')
    #     self.assertTrue(logged)
    #
    #     response = self.client.get(reverse('qs_accounts:signin'))
    #     self.assertStatusCode(response, 302)
    #     self.assertIn(resolve_url(settings.LOGIN_REDIRECT_URL), response['location'])
    #
    #     response = self.client.get(reverse('qs_accounts:signup'))
    #     self.assertStatusCode(response, 302)
    #     self.assertIn(resolve_url(settings.LOGIN_REDIRECT_URL), response['location'])


class AccountTemplateTagsTest(BaseTestCase):

    @override_settings(AUTHENTICATION_BACKENDS=('social.backends.twitter.TwitterOAuth',
                                                'django.contrib.auth.backends.ModelBackend'))
    def test_get_backends(self):
        backends = get_social_backends()
        self.assertTrue('twitter' in backends)
        self.assertEquals(len(backends), 1)


class SocialAuthErrorsViewTest(BaseTestCase):
    def setUp(self):
        super(SocialAuthErrorsViewTest, self).setUp()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(email="test@example.com", password="secret")

    def test_redirection_user_not_authenticated(self):
        response = self.client.get(reverse('qs_accounts:social-auth-errors'))
        self.assertStatusCode(response, 302)
        self.assertIn(resolve_url(reverse('qs_accounts:signup')), response['location'])

    def test_redirection_user_not_authenticated_keep_querystring(self):
        response = self.client.get(reverse('qs_accounts:social-auth-errors') + '?foo=bar')
        self.assertStatusCode(response, 302)
        self.assertIn(resolve_url(reverse('qs_accounts:signup')), response['location'])
        self.assertIn('?foo=bar', response['location'])

    def test_redirection_user_authenticated(self):
        logged = self.client.login(username=self.user.email, password='secret')
        self.assertTrue(logged)

        response = self.client.get(reverse('qs_accounts:social-auth-errors'))
        self.assertStatusCode(response, 302)
        self.assertIn(resolve_url(reverse('qs_accounts:profile-social')), response['location'])


class GetSocialMessageErrorsTest(BaseTestCase):

    def test_get_social_message_errors_empty(self):
        request = RequestFactory().get('/')
        msgs = get_social_message_errors(request)
        self.assertEquals(msgs, [])

    def test_get_social_message_errors(self):
        request = RequestFactory().get('/')
        # RequestFactory is very limited, so we have to tweak this request in order to work with
        # messages middleware
        request.session = {}
        request._messages = FallbackStorage(request)

        messages.add_message(request, messages.ERROR, 'test')
        msgs = get_social_message_errors(request)
        self.assertEquals(len(msgs), 1)
        self.assertEquals(msgs[0].message, 'test')
        self.assertEquals(msgs[0].level, messages.ERROR)

    def test_get_social_message_errors_with_other_messages(self):
        request = RequestFactory().get('/')
        request.session = {}
        request._messages = FallbackStorage(request)

        messages.add_message(request, messages.ERROR, 'test')
        messages.add_message(request, messages.INFO, 'info')
        msgs = get_social_message_errors(request)
        self.assertEquals(len(msgs), 1)
        self.assertEquals(msgs[0].message, 'test')
        self.assertEquals(msgs[0].level, messages.ERROR)

    def test_get_social_message_errors_querystring(self):
        request = RequestFactory().get('/?message=test-query-string')
        msgs = get_social_message_errors(request)
        self.assertEquals(len(msgs), 1)
        self.assertEquals(msgs[0], 'test-query-string')

    def test_get_social_message_errors_ignore_querystring(self):
        request = RequestFactory().get('/?message=test-query-string')
        request.session = {}
        request._messages = FallbackStorage(request)

        messages.add_message(request, messages.ERROR, 'test')
        msgs = get_social_message_errors(request)
        self.assertEquals(len(msgs), 1)
        self.assertEquals(msgs[0].message, 'test')
        self.assertEquals(msgs[0].level, messages.ERROR)
