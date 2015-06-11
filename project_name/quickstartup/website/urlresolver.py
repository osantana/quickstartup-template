# coding: utf-8


from django.core.urlresolvers import NoReverseMatch

from .models import Page


def page_reverse(slug):
    page = Page.objects.filter(slug=slug).first()

    if not page:
        raise NoReverseMatch("Page {!r} not found.".format(slug))

    return page.get_absolute_url()
