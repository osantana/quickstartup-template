# coding: utf-8


from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import RequestContext, TemplateDoesNotExist
from django.template.loader import render_to_string


class SendMailException(Exception):
    pass


def send_transaction_mail(user, template_name, request=None, site=None,
                          template_base="mails/{}.{}",
                          subject_template_base="mails/{}-subject.txt",
                          **context):
    if request is not None:
        context = RequestContext(request, context)
        site = get_current_site(request)

    if site is None:
        raise SendMailException("Cannot get current site.")

    context.update({'user': user, 'site': site})

    subject = render_to_string(subject_template_base.format(template_name, "txt"), context)
    subject = ''.join(subject.splitlines())

    from_email = settings.DEFAULT_FROM_EMAIL
    message_txt = render_to_string(template_base.format(template_name, "txt"), context)
    email_message = EmailMultiAlternatives(subject, message_txt, from_email, [user.email])

    try:
        message_html = render_to_string(template_base.format(template_name, "html"), context)
    except TemplateDoesNotExist:
        pass
    else:
        email_message.attach_alternative(message_html, 'text/html')

    email_message.send()
