# coding: utf-8


from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext, Template, loader
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login

from .forms import ContactForm
from .models import Page


DEFAULT_TEMPLATE = 'website/page.html'


@csrf_protect
def website_page(request, url):
    if not url.startswith('/'):
        url = '/' + url

    if not url.endswith('/'):
        url += "/"

    page = get_object_or_404(Page, url__exact=url)

    if page.registration_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)

    page_context = RequestContext(request, {'page': page})

    context = RequestContext(request, {
        'page': page,
        'title': Template(page.title).render(page_context),
        'content': Template(page.content).render(page_context),
    })

    if page.template_name:
        template = loader.select_template((page.template_name, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)

    response = HttpResponse(template.render(context))
    return response


@csrf_protect
def contact(request, post_contact_redirect=None, form_class=ContactForm, template_name="website/contact.html"):
    if post_contact_redirect is None:
        post_contact_redirect = reverse("contact")

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your message was sent successfully!"))
            return redirect(post_contact_redirect)
    else:
        form = form_class()

    return render(request, template_name, {"form": form})
