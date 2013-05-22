# coding: utf-8


from django import forms
from django.utils.safestring import mark_safe

from .django_quickstartup.quickstartup.utils import get_anticaptcha_tokens


class EmailInput(forms.TextInput):
    input_type = "email"


class PhoneInput(forms.TextInput):
    input_type = "tel"


class AntiCaptchaWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        output = '''<script>document.write('<input type="hidden" name="anticaptcha" value="%s"/>')</script>
        ''' % (get_anticaptcha_tokens()[0],)
        return mark_safe(output)