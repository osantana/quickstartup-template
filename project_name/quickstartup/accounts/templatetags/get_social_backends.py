# coding: utf-8


from django.conf import settings
from django import template

from social.backends.utils import load_backends

register = template.Library()


@register.assignment_tag
def get_social_backends(*args, **kwargs):
    """Returns a dictionary of social enabled backends, in the form: {'backend name': backend class }"""
    return load_backends(settings.AUTHENTICATION_BACKENDS)
