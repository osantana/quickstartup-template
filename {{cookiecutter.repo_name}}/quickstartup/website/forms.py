# coding: utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext

from ..commons.fields import AntiCaptchaField
from ..commons.widgets import EmailInput, PhoneInput

from .models import Page, Contact


class PageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/\.~]+$')

    class Meta:
        model = Page

    def clean_url(self):
        url = self.cleaned_data['url']

        if not url.startswith('/'):
            raise forms.ValidationError(ugettext("URL is missing a leading slash."))

        if not url.endswith('/'):
            raise forms.ValidationError(ugettext("URL is missing a trailing slash."))

        return url


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "phone", "message", "anticaptcha")

    email = forms.EmailField(label=_("email"), max_length=255, widget=EmailInput)
    phone = forms.CharField(label=_("phone"), max_length=100, widget=PhoneInput, required=False)
    message = forms.CharField(label=_("message"), widget=forms.Textarea(attrs={"class": "input-block-level"}))
    anticaptcha = AntiCaptchaField()