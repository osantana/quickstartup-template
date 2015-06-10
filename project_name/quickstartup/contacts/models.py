# coding: utf-8


from django.conf import settings
from django.core.urlresolvers import reverse
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


class Contact(models.Model):
    status = models.CharField(_("status"), max_length=1, choices=CONTACT_STATUS, default="N")
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"), max_length=255)
    phone = models.CharField(_("phone"), max_length=100, blank=True)
    message = models.TextField(_("message"))

    @property
    def admin_url(self):
        return reverse("admin:contacts_contact_change", args=(self.pk,))


def send_contact_mail(instance, created, **kwargs):
    if not created:
        return

    template = _(
        "Contact From: {instance.name} <{instance.email}>\n"
        "Phone: {instance.phone}\n"
        "Message:\n"
        "{instance.message}\n"
        "URL: http://{domain}{instance.admin_url}\n"
    )

    domain = settings.PROJECT_DOMAIN
    email = EmailMessage(
        subject=_("New Contact from %s") % (settings.PROJECT_NAME,),
        body=template.format(domain=domain, instance=instance),
        from_email=instance.email,
        to=[settings.PROJECT_CONTACT],
        headers={"Reply-To": instance.email},
    )

    email.send(fail_silently=True)


post_save.connect(send_contact_mail, Contact, dispatch_uid="quickstartup.contacts")
