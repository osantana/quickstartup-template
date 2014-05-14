# coding: utf-8


import os
import re

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.http import Http404
from django.template import loader


NAME_REGEX = re.compile(r'^[-a-z0-9]+$')
_cache_page_list = None


def valid_name(page_name):
    return NAME_REGEX.match(page_name)


def _load_pages():
    global _cache_page_list

    page_list = []
    for path in settings.TEMPLATE_DIRS:
        for filename in os.listdir("{}/website/pages".format(path)):
            page_name = os.path.splitext(filename)[0]
            if valid_name(page_name):
                page_list.append(page_name)

    _cache_page_list = tuple(page_list)


def list_pages():
    if _cache_page_list is not None:
        return _cache_page_list

    _load_pages()

    return _cache_page_list


def flush_pages_cache():
    global _cache_page_list
    _cache_page_list = None


def page_reverse(page_name):
    if not valid_name(page_name):
        raise NoReverseMatch("Invalid page name: {}. It must match regex /[-\w]/.".format(page_name))

    if page_name not in list_pages():
        raise NoReverseMatch("Invalid page name: {}. Missing template.".format(page_name))

    return "/{}/".format(page_name)


def get_template(path):
    name = path.strip("/")

    if not valid_name(name):
        raise Http404()

    if name not in list_pages():
        raise Http404()

    template_name = "website/pages/{}.html".format(name)
    return loader.get_template(template_name)
