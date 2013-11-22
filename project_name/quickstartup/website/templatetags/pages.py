# coding: utf-8


from django import template
from django.shortcuts import get_object_or_404

from ..models import Page


register = template.Library()


class PageUrlNode(template.Node):
    def __init__(self, page_name):
        self.page_name = page_name

    def render(self, context):
        page = get_object_or_404(Page, name=self.page_name)
        return page.url


@register.tag
def page_url(parser, token):
    try:
        tag_name, page_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("page_url tag requires page name")

    if not (page_name[0] == page_name[-1] and page_name[0] in ('"', "'")):
        raise template.TemplateSyntaxError("page name should be in quotes")

    return PageUrlNode(page_name.strip("\"'"))
