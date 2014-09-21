# coding: utf-8


from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import override_settings

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

        message = mail.outbox[0]
        self.assertIn("Hi,", message.text)
        self.assertIn("<h3>Hi,</h3>", message.html)

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

        message = mail.outbox[0]
        self.assertIn("Hi John Doe,", message.text)
        self.assertIn("<h3>Hi John Doe,</h3>", message.html)

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
        self.assertEqual(user.activation_key_expired(), False)

        message = mail.outbox[0]
        self.assertIn("Hi John Doe,")
        self.assertIn("<h3>Hi John Doe,</h3>", message.html)
        self.fail()