# coding: utf-8


from django import forms

from .models import Page


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ("slug", "template_name", "login_required")
