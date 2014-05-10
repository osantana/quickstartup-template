# coding: utf-8


from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .forms import ContactForm
from .urlresolver import get_template


def website_page(request, path):
    template = get_template(path)
    page_context = RequestContext(request, {'path': path})
    response = HttpResponse(template.render(page_context))
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


def homepage(request):
    return render(request, "website/homepage.html")
