# coding: utf-8


from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .forms import ContactForm


class ContactView(CreateView):
    template_name = 'contacts/contact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse("qs_contacts:contact")

    def form_valid(self, form):
        messages.success(self.request, _("Your message was sent successfully!"))
        return super(ContactView, self).form_valid(form)
