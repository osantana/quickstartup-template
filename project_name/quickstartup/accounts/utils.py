# -*- coding: utf-8 -*-

from django.contrib import messages


def get_social_message_errors(request):
    # reference:
    # http://python-social-auth.readthedocs.org/en/latest/configuration/django.html#exceptions-middleware
    msgs = messages.get_messages(request)
    error_messages = []
    for msg in msgs:
        if msg.level == messages.ERROR:
            error_messages.append(msg)
    if not error_messages and request.GET.get('message', ''):
        error_messages = [request.GET.get('message')]
    return error_messages
