# coding: utf-8


from django.conf import settings
from django.core.mail import get_connection
from django.template import Context

from quickstartup.messages import HTMLMessage


def send_activation_email(user, extra_info, *args, **kwargs):

    # TODO: improve these hardcoded templates
    email_template_name = "mails/password-reset.txt"
    html_email_template_name = "mails/password-reset.html"
    subject_template_name = "mails/password-reset-subject.txt"

    context = Context({
        'email': user.email,
        'user_account': user,
        'extra_info': extra_info,
    })

    message = HTMLMessage(settings.DEFAULT_FROM_EMAIL, user.email,
                          subject_template_name,
                          email_template_name,
                          html_email_template_name, context)

    connection = get_connection()
    connection.send_messages([message])
