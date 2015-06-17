# coding: utf-8


from django import forms
from django.utils.translation import ugettext_lazy as _

from ..security import get_antispam_tokens
from ..widgets import AntiSpamWidget


ERROR_MESSAGE = _(u'You need to enable JavaScript to complete this form.')


class AntiSpamField(forms.CharField):
    widget = AntiSpamWidget
    default_error_messages = {
        'required': ERROR_MESSAGE,
    }

    def clean(self, value):
        value = super(AntiSpamField, self).clean(value)

        if value not in get_antispam_tokens():
            raise forms.ValidationError(ERROR_MESSAGE)
