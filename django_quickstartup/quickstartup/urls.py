# coding: utf-8


from django.conf.urls import patterns, url

from .forms import CustomAuthenticationForm


urlpatterns = patterns('',
    url(r"^accounts/signin/$", "django.contrib.auth.views.login",
        {"template_name": "website/signin.html", "authentication_form": CustomAuthenticationForm},
        name="signin"),
    url(r"^accounts/signup/$", "django_quickstartup.quickstartup.views.boilerplate", name="signup"),
    url(r"^account/logout/$", "django.contrib.auth.views.logout", {"next_page": "/"}, name="logout"),
    url(r"^accounts/profile/$", "django_quickstartup.quickstartup.views.profile", name="profile"),

    url(r'^password/reset/$', "django_quickstartup.quickstartup.views.password_reset", name="password-reset"),

    url(r'^password/reset/done/$', "django.contrib.auth.views.password_reset_done",
        {"template_name": "website/reset-done.html"},
        name="password-reset-done"),

    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        "django.contrib.auth.views.password_reset_confirm", {"template_name": "website/reset-confirm.html"},
        name='password_reset_confirm'),

    url(r'^password/reset/complete/$', "django.contrib.auth.views.password_reset_complete",
        {"template_name": "website/reset-complete.html"},
        name='password_reset_complete'),

    # url(r'^password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    # url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done',name='password_change_done'),

    url(r'^contact/$', "django_quickstartup.quickstartup.views.boilerplate", name="contact"),
    url(r'^app/', 'django_quickstartup.quickstartup.views.dashboard', name="dashboard"),  # to be override...
    url(r'^(?P<url>.*)$', "django_quickstartup.quickstartup.views.website_page", name="page"),
)
