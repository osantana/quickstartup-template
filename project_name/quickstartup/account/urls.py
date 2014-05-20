# coding: utf-8


from django.conf.urls import patterns, url

from .forms import CustomAuthenticationForm, CustomSetPasswordForm


urlpatterns = patterns('',
    url(r"^signin/$", "django.contrib.auth.views.login",
        {"template_name": "account/signin.html", "authentication_form": CustomAuthenticationForm},
        name="signin"),
    url(r"^logout/$", "django.contrib.auth.views.logout", {"next_page": "/"}, name="logout"),

    url(r"^password/reset/$", "quickstartup.account.views.password_reset", name="password_reset"),
    url(r"^password/reset/done/$", "django.contrib.auth.views.password_reset_done",
        {"template_name": "account/reset-done.html"},
        name="password_reset_done"),
    url(r"^password/reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        "django.contrib.auth.views.password_reset_confirm",
        {"template_name": "account/reset-confirm.html",
         "set_password_form": CustomSetPasswordForm,
         "post_reset_redirect": "qs_accounts:password_reset_complete"},
        name="password_reset_confirm"),
    url(r"^password/reset/complete/$", "django.contrib.auth.views.password_reset_complete",
        {"template_name": "account/reset-complete.html"},
        name="password_reset_complete"),

    # TODO:
    url(r"^signup/$", "quickstartup.account.views.signup", name="signup"),
    url(r"^profile/$", "quickstartup.account.views.profile", name="profile"),
    url(r"^password/change/$", "django.contrib.auth.views.password_change", name="password_change"),
    url(r"^password/change/done/$", "django.contrib.auth.views.password_change_done", name="password_change_done"),
)
