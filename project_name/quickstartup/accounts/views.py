# coding: utf-8
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, resolve_url
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from .forms import (CustomPasswordResetForm, CustomSetPasswordForm,
                    CustomUserProfileForm)


def signup(request, *args, **kwargs):
    return render(request, "accounts/signup.html", kwargs)


@login_required
def profile(request, *args, **kwargs):
    return render(request, "accounts/profile.html", kwargs)


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


@csrf_protect
@login_required
def profile(request, *args, **kwargs):
    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Succesfully updated profile.'))

        # skip password_form if the user does not try to change it
        data = request.POST
        if not (request.POST['new_password1'] or request.POST['new_password2']):
            data = None

        password_form = CustomSetPasswordForm(request.user, data)
        if password_form.is_valid():
            messages.success(request, _(u'Succesfully updated your password.'))
            password_form.save()

    else:
        form = CustomUserProfileForm(instance=request.user)
        password_form = CustomSetPasswordForm(user=request.user)

    context = {
        "form": form,
        "password_form": password_form,
    }
    return render(request, 'accounts/profile.html', context)
