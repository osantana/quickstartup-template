# coding: utf-8


from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from social.backends.utils import load_backends


admin.autodiscover()

urlpatterns = patterns("")


if settings.ADMIN_URL:
    urlpatterns += patterns(
        "",  # prefix
        url(r"^{}/".format(settings.ADMIN_URL), include(admin.site.urls)),
    )


urlpatterns += patterns(
    '',  # prefix
    url(r"^accounts/", include("quickstartup.accounts.urls", namespace="qs_accounts")),
    url(r"^contact/$", include("quickstartup.contacts.urls", namespace="qs_contacts")),
    url(r"^", include("quickstartup.website.urls", namespace="qs_pages")),
)


# social authentication
if load_backends(settings.AUTHENTICATION_BACKENDS):
    urlpatterns += patterns(
        "",  # prefix
        url(r"^", include('social.apps.django_app.urls', namespace='social')),
    )
