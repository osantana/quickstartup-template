# coding: utf-8

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import login as auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, resolve_url
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import UpdateView, TemplateView
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import ugettext_lazy as _
from braces.views import LoginRequiredMixin
from registration.backends.default.views import ActivationView

from .forms import CustomPasswordResetForm
from .utils import get_social_message_errors


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    return auth_login(request, *args, **kwargs)


@csrf_protect
def password_reset(request, template_name="accounts/reset.html", mail_template_name="password-reset",
                   password_reset_form=CustomPasswordResetForm,
                   post_reset_redirect=None, extra_context=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse("qs_accounts:password_reset_done")
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)

    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            form.save(request, mail_template_name)
            return redirect(post_reset_redirect)
    else:
        form = password_reset_form()

    context = {'form': form}
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


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


class UserSocialProfile(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super(UserSocialProfile, self).get_context_data(**kwargs)
        context['error_messages'] = get_social_message_errors(self.request)
        return context


@never_cache
def social_auth_errors(request, default_redirect='qs_accounts:signup'):
    """Handles social auth errors. Some assumptions here is:
        - If the user is authenticated, then he will be redirected to social profile view
        - If the user is not authenticated, then he will be redirect to the <default_redirect> view,
          defaults to sign-up view
    """
    if request.user.is_authenticated():
        url = reverse('qs_accounts:profile-social')
    else:
        url = reverse(default_redirect)

    args = request.META.get('QUERY_STRING', '')
    if args:
        url = '{}?{}'.format(url, args)

    return redirect(url)


class SignupActivationView(ActivationView):
    def activate(self, request, activation_key):
        activated_user = super().activate(request, activation_key)

        if activated_user:
            site = get_current_site(request)
            messages.success(request, _("Welcome to {}! Your account was successfully activated.".format(site.name)))

        return activated_user

    def get_success_url(self, request, user):
        return settings.LOGIN_REDIRECT_URL, (), {}
