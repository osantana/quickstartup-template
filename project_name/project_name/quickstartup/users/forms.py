# coding: utf-8


from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import get_connection
from django.template import RequestContext
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm, AuthenticationForm, SetPasswordForm

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
    username = forms.EmailField(label=_("E-Mail"), max_length=254, widget=EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={"class": "form-control"}))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("E-Mail"), max_length=254, widget=EmailInput(attrs={"class": "form-control"}))

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.txt',
             html_email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):

        context = RequestContext(request)

        user_model = get_user_model()
        email = self.cleaned_data["email"]
        active_users = user_model.objects.filter(email__iexact=email, is_active=True)
        for user in active_users:
            if not user.has_usable_password():
                continue

            context.update({
                'email': user.email,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            })

            message = HTMLMessage(settings.DEFAULT_FROM_EMAIL, user.email, subject_template_name, email_template_name,
                                  html_email_template_name, context)

            connection = get_connection()
            connection.send_messages([message])


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput(attrs={"class": "form-control"}))


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'groups', 'user_permissions',
                   'created', 'is_active', 'is_staff', 'activation_key', 'password']
