# coding: utf-8


from django.conf.urls import patterns, url

from .forms import CustomAuthenticationForm, CustomSetPasswordForm


urlpatterns = patterns('',
    url(r"^signin/$", "django.contrib.auth.views.login",
        {"template_name": "website/signin.html", "authentication_form": CustomAuthenticationForm},
        name="signin"),
    url(r"^logout/$", "django.contrib.auth.views.logout", {"next_page": "/"}, name="logout"),

    url(r'^password/reset/$', "quickstartup.users.views.password_reset", name="password-reset"),
    url(r'^password/reset/done/$', "django.contrib.auth.views.password_reset_done",
        {"template_name": "website/reset-done.html"},
        name="password-reset-done"),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        "django.contrib.auth.views.password_reset_confirm",
        {"template_name": "website/reset-confirm.html", "set_password_form": CustomSetPasswordForm},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$', "django.contrib.auth.views.password_reset_complete",
        {"template_name": "website/reset-complete.html"},
        name='password_reset_complete'),

    # TODO:
    url(r"^signup/$", "quickstartup.users.views.signup", name="signup"),
    url(r"^profile/$", "quickstartup.users.views.profile", name="profile"),
    url(r'^password/change/$', 'django.contrib.auth.views.password_change', name='password-change'),
    url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done', name='password-change-done'),
)
