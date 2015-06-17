# coding: utf-8


import mock

from django.core import mail
from django.core.urlresolvers import reverse

from ..tests.base import BaseTestCase, TEST_ROOT_DIR

from .models import Contact


TEMPLATE_DIRS = (
    str(TEST_ROOT_DIR / "templates"),
)


class ContactTest(BaseTestCase):
    @mock.patch("quickstartup.core.fields.AntiSpamField.clean")
    def test_send_contact(self, patched_clean):
        patched_clean.return_value = "1337"
        data = {
            "name": u"John Doe",
            "email": u"john@doe.com",
            "phone": u"+1 55 555-1234",
            "message": u"Hello World!",
            "antispam": u"1337",
        }

        url = reverse("qs_contacts:contact")
        response = self.client.post(url, data, follow=True)
        self.assertStatusCode(response, 200)
        self.assertTemplateUsed(response, "contacts/contact.html")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, u'New Contact from Django Quickstartup')
        self.assertTrue(u"Contact From: John Doe <john@doe.com>" in mail.outbox[0].body)
        self.assertTrue(u"Phone: +1 55 555-1234" in mail.outbox[0].body)
        self.assertTrue(u"Message:\nHello World!" in mail.outbox[0].body)

        contact = Contact.objects.first()
        self.assertEquals(contact.name, u"John Doe")
        self.assertEquals(contact.email, u"john@doe.com")
        self.assertEquals(contact.phone, u"+1 55 555-1234")
        self.assertEquals(contact.message, u"Hello World!")
        self.assertEquals(contact.status, "N")

    def test_fail_antispam(self):
        data = {
            "name": u"John Doe",
            "email": u"john@doe.com",
            "phone": u"+1 55 555-1234",
            "message": u"Hello World!",
            "antispam": u"1337",
        }

        url = reverse("qs_contacts:contact")
        response = self.client.post(url, data, follow=True)
        self.assertFormError(response, 'form', 'antispam', u'You need to enable JavaScript to complete this form.')

    def test_access_an_existent_url(self):
        response = self.client.get("/contact/")
        self.assertStatusCode(response, 200)
        self.assertTemplateUsed(response, "contacts/contact.html")

    def test_send_email_once(self):
        contact = Contact.objects.create(name="John Doe",
                                         email="john@doe.com",
                                         message="Hello!")
        self.assertEquals(len(mail.outbox), 1)

        contact.message = "Hello World!"
        contact.save()
        self.assertEquals(len(mail.outbox), 1)  # changes don't send a new mail

    def test_url_in_admin(self):
        contact = Contact.objects.create(name="John Doe",
                                 email="john@doe.com",
                                 message="Hello!")

        message = mail.outbox[0].body
        self.assertIn("http://localhost:8000/admin/contacts/contact/{}/".format(contact.pk), message)
