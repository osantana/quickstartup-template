# coding: utf-8


from django import template
from django.http import Http404

from ..models import Page


register = template.Library()


@register.simple_tag
def page_url(page_name):
    try:
        page = Page.objects.get(name=page_name)
    except Page.DoesNotExist:
        raise Http404("Page '%s' not found." % (page_name,))

    return page.url
