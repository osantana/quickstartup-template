# coding: utf-8


from django import forms
from django.conf import settings
from django.core.mail import get_connection
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm, AuthenticationForm

from ..commons.messages import HTMLMessage
from ..commons.widgets import EmailInput
from .models import User


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('password (verify)'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)

        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User

    def clean_password(self):
        return self.initial["password"]


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, widget=EmailInput())


class CustomPasswordResetForm(PasswordResetForm):
    def notify(self, context, token_generator, subject_template_name, email_template_name, html_email_template_name,
               use_https):
        for user in self.users_cache:
            context.update({
                "user": user,
                "token": token_generator.make_token(user),
                "uid": int_to_base36(user.pk),
                "protocol": use_https and 'https' or 'http',
            })

            message = HTMLMessage(settings.DEFAULT_FROM_EMAIL, user.email, subject_template_name, email_template_name,
                                  html_email_template_name, context)

            connection = get_connection()
            connection.send_messages([message])
