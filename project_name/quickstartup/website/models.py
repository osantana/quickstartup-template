# coding: utf-8

from django.conf import settings
from django.db import models
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


CONTACT_STATUS = (
    ("N", _("New")),
    ("O", _("Ongoing")),
    ("R", _("Resolved")),
    ("C", _("Closed")),
    ("I", _("Invalid")),
)


class Page(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    url = models.CharField(_("URL"), max_length=255, unique=True, db_index=True)
    title = models.CharField(_("title"), max_length=255, blank=True)
    content = models.TextField(_("content"), blank=True)
    template_name = models.CharField(_("template"), max_length=70, blank=True)
    registration_required = models.BooleanField(_("registration required"), default=False)

    class Meta:
        ordering = ('name',)

    def __repr__(self):
        return "<Page: %s url: %s>" % (self.name, self.url)

    def get_absolute_url(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.url.replace("/", "-").strip("-")

        return super(Page, self).save(*args, **kwargs)


class Contact(models.Model):
    status = models.CharField(_("status"), max_length=1, choices=CONTACT_STATUS, default="N")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"), max_length=255)
    phone = models.CharField(_("phone"), max_length=100, blank=True)
    message = models.TextField(_("message"))


def send_contact_mail(instance, created, **kwargs):
    if not created:
        return

    template = _(
        "Contact From: {instance.name} <{instance.email}>\n"
        "Phone: {instance.phone}\n"
        "Message:\n"
        "{instance.message}"
    )

    email = EmailMessage(
        subject=_("New Contact from %s") % (settings.PROJECT_NAME,),
        body=template.format(instance=instance),
        from_email=instance.email,
        to=[settings.PROJECT_CONTACT],
        headers={"Reply-To": instance.email},
    )

    email.send(fail_silently=True)


if settings.DEFAULT_TRANSACTIONAL_EMAIL.get("contact"):
    post_save.connect(send_contact_mail, Contact, dispatch_uid="quickstartup.contact")
