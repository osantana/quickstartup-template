# coding: utf-8


from django import template

from quickstartup.website.urlresolver import page_reverse


register = template.Library()


@register.simple_tag
def page_url(page_name):
    return page_reverse(page_name)
