# coding: utf-8


from django.conf.urls import patterns, url
from django.contrib.auth.forms import PasswordChangeForm

from .forms import CustomAuthenticationForm, CustomSetPasswordForm, CustomUserProfileForm
from .views import UserProfile, UserSecurityProfile, UserSocialProfile


urlpatterns = patterns('',
    url(r"^signin/$", "quickstartup.accounts.views.login",
        {"template_name": "accounts/signin.html", "authentication_form": CustomAuthenticationForm},
        name="signin"),
    url(r"^logout/$", "django.contrib.auth.views.logout", {"next_page": "/"}, name="logout"),

    url(r"^password/reset/$", "quickstartup.accounts.views.password_reset", name="password_reset"),
    url(r"^password/reset/done/$", "django.contrib.auth.views.password_reset_done",
        {"template_name": "accounts/reset-done.html"},
        name="password_reset_done"),
    url(r"^password/reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        "django.contrib.auth.views.password_reset_confirm",
        {"template_name": "accounts/reset-confirm.html",
         "set_password_form": CustomSetPasswordForm,
         "post_reset_redirect": "qs_accounts:password_reset_complete"},
        name="password_reset_confirm"),
    url(r"^password/reset/complete/$", "django.contrib.auth.views.password_reset_complete",
        {"template_name": "accounts/reset-complete.html"},
        name="password_reset_complete"),

    url(r"^signup/$", "quickstartup.accounts.views.signup", name="signup"),
    # TODO: signup activation
    # url(r"^signup/activation/$", "quickstartup.accounts.views.signup_activation", name="activation"),

    url(r"^profile/$",
        UserProfile.as_view(template_name='accounts/profile.html',
                            form_class=CustomUserProfileForm), name="profile"),
    url(r"^profile/security/$",
        UserSecurityProfile.as_view(template_name='accounts/profile-security.html',
                                    form_class=PasswordChangeForm,
                                    form_class_without_password=CustomSetPasswordForm),
        name="profile-security"),
    url("^profile/social/$",
        UserSocialProfile.as_view(template_name='accounts/profile-social.html'),
        name='profile-social'),
    url("^social-auth-errors/$", "quickstartup.accounts.views.social_auth_errors",
        name='social-auth-errors'),
    url(r"^password/change/$", "django.contrib.auth.views.password_change", name="password_change"),
    url(r"^password/change/done/$", "django.contrib.auth.views.password_change_done", name="password_change_done"),
)
