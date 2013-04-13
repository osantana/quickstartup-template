# coding: utf-8
from django import forms


class HTML5Email(forms.TextInput):
    input_type = "email"