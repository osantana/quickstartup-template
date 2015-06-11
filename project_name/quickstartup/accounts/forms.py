# coding: utf-8


from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import get_connection
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm, AuthenticationForm, SetPasswordForm

from ..messages import HTMLMessage
from ..widgets import EmailInput
from .models import User


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password (verify)'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password (verify)'), widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user_model = get_user_model()
        user = user_model.objects.create_user(email=self.cleaned_data["email"],
                                              password=self.cleaned_data["password1"],
                                              name=self.cleaned_data["name"],
                                              commit=commit)
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("name", "email", "password")

    def clean_password(self):
        return self.initial["password"]


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("E-Mail"), max_length=254, widget=EmailInput())
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("E-Mail"), max_length=254, widget=EmailInput())

    # TODO: remove this "extra arguments" from here and move the messaging to a signal handler
    # TODO: move signal dispatch to model instead of form...
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
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            path = reverse("qs_accounts:password_reset_confirm",
                           kwargs={"uidb64": uid, "token": token})

            context.update({
                'email': user.email,
                'uid': uid,
                'user_account': user,
                'token': token,
                'protocol': 'https' if use_https else 'http',
                'path': path,
            })

            message = HTMLMessage(settings.DEFAULT_FROM_EMAIL, user.email, subject_template_name, email_template_name,
                                  html_email_template_name, context)

            connection = get_connection()
            connection.send_messages([message])

        # TODO: use this method to send message
        # ctx_dict = {}
        # if request is not None:
        #     ctx_dict = RequestContext(request, ctx_dict)
        # # update ctx_dict after RequestContext is created
        # # because template context processors
        # # can overwrite some of the values like user
        # # if django.contrib.auth.context_processors.auth is used
        # ctx_dict.update({
        #     'user': self.user,
        #     'activation_key': self.activation_key,
        #     'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
        #     'site': site,
        # })
        # subject = getattr(settings, 'REGISTRATION_EMAIL_SUBJECT_PREFIX', '') + \
        #           render_to_string('registration/activation_email_subject.txt', ctx_dict)
        # # Email subject *must not* contain newlines
        # subject = ''.join(subject.splitlines())
        # from_email = getattr(settings, 'REGISTRATION_DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
        # message_txt = render_to_string('registration/activation_email.txt', ctx_dict)
        #
        # email_message = EmailMultiAlternatives(subject, message_txt, from_email, [self.user.email])
        #
        # if getattr(settings, 'REGISTRATION_EMAIL_HTML', True):
        #     try:
        #         message_html = render_to_string('registration/activation_email.html', ctx_dict)
        #     except TemplateDoesNotExist:
        #         pass
        #     else:
        #         email_message.attach_alternative(message_html, 'text/html')
        #
        # email_message.send()

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput())
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput())


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "email")
