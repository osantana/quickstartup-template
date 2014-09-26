# coding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import login as auth_login
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect, resolve_url
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import UpdateView, TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from .forms import CustomPasswordResetForm, CustomUserCreationForm


@sensitive_post_parameters()
@csrf_protect
@never_cache
def signup(request, template_name='accounts/signup.html', redirect_to="qs_accounts:signin",
           signup_form=CustomUserCreationForm, extra_context=None):
    if request.user.is_authenticated():
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    if request.method == "POST":
        form = signup_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            url = reverse(redirect_to) if redirect_to.startswith("/") else redirect_to
            return redirect(url)

    else:
        form = signup_form()

    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, context)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    return auth_login(request, *args, **kwargs)


@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name="accounts/reset.html",
                   subject_template_name="mails/password-reset-subject.txt",
                   text_email_template_name="mails/password-reset.txt",
                   html_email_template_name="mails/password-reset.html",
                   password_reset_form=CustomPasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse("qs_accounts:password_reset_done")
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)

    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': text_email_template_name,
                'html_email_template_name': html_email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return redirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)


class ProfileMixin(object):
    def get_object(self, *args, **kwargs):
        return self.request.user


class UserProfile(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, _(u'Succesfully updated profile.'))
        return super(UserProfile, self).form_valid(form)


class UserSecurityProfile(LoginRequiredMixin, ProfileMixin, UpdateView):
    success_url = reverse_lazy('qs_accounts:profile-security')
    form_class_without_password = None

    def get_form_class(self):
        # Probably, user was authenticated with social auth
        if not self.request.user.has_usable_password():
            return self.form_class_without_password or self.form_class
        return self.form_class

    def form_valid(self, form):
        messages.success(self.request, _(u'Succesfully updated your password.'))
        return super(UserSecurityProfile, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UserSecurityProfile, self).get_form_kwargs()
        kwargs.update({'user': self.object})
        if 'instance' in kwargs:
            del kwargs['instance']
        return kwargs


class UserSocialProfile(LoginRequiredMixin, ProfileMixin, TemplateView):
    pass
