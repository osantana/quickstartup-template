# coding: utf-8


from django import forms
from django.utils.safestring import mark_safe

from .security import get_antispam_tokens


class EmailInput(forms.TextInput):
    input_type = "email"


class PhoneInput(forms.TextInput):
    input_type = "tel"


class AntiSpamWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        output = '''<script>document.write('<input type="hidden" name="antispam" value="%s"/>')</script>
        ''' % (get_antispam_tokens()[0],)
        return mark_safe(output)
