# coding: utf-8


from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404

from .models import Page


def website_page(request, path):
    slug = path.strip("/")
    page = get_object_or_404(Page, slug=slug)
    template = loader.get_template(page.template)
    context = RequestContext(request, {"page": page, "slug": slug, "path": path})
    response = HttpResponse(template.render(context))
    return response


def index(request):
    # TODO: check if user is logged
    return render(request, "website/index.html")
