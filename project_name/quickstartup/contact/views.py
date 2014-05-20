# coding: utf-8


from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .forms import ContactForm


@csrf_protect
def contact(request, post_contact_redirect=None, form_class=ContactForm, template_name="contact/contact.html"):
    if post_contact_redirect is None:
        post_contact_redirect = reverse("qs_contacts:contact")

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your message was sent successfully!"))
            return redirect(post_contact_redirect)
    else:
        form = form_class()

    return render(request, template_name, {"form": form})
