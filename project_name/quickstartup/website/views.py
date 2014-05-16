# coding: utf-8


from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

from .urlresolver import get_template


def website_page(request, path):
    template = get_template(path)
    page_context = RequestContext(request, {'path': path})
    response = HttpResponse(template.render(page_context))
    return response


def homepage(request):
    # TODO: check if user is logged
    return render(request, "website/homepage.html")
