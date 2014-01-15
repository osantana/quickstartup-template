# coding: utf-8


from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required

from .forms import CustomPasswordResetForm


# User
def signup(request, *args, **kwargs):
    return render(request, "website/page.html", kwargs)


@csrf_protect
def password_reset(request, post_reset_redirect=None, form_class=CustomPasswordResetForm,
                   template_name="website/reset.html",
                   subject_template_name="website/mail/password-reset-subject.txt",
                   text_email_template_name="website/mail/password-reset.txt",
                   html_email_template_name="website/mail/password-reset.html"):
    if post_reset_redirect is None:
        post_reset_redirect = reverse("password-reset-done")

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            context = RequestContext(request)
            form.notify(
                context=context,
                token_generator=default_token_generator,
                subject_template_name=subject_template_name,
                email_template_name=text_email_template_name,
                html_email_template_name=html_email_template_name,
                use_https=request.is_secure(),
            )
            return redirect(post_reset_redirect)
    else:
        form = form_class()

    return render(request, template_name, {'form': form})


@login_required
def profile(request, *args, **kwargs):
    return render(request, "app/profile.html", kwargs)
