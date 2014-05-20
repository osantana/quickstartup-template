# coding: utf-8


from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # QUICKSTARTUP: Replace the url mapping bellow with your application urls module
    url("^", include("apps.sample.urls", namespace="app")),

    # Django Admin Interface
    url(r"^admin/", include(admin.site.urls)),

    # This url mappings must be the last one
    url(r"^accounts/", include("quickstartup.accounts.urls", namespace="qs_accounts")),
    url(r"^contact/$", include("quickstartup.contacts.urls", namespace="qs_contacts")),
    url(r"^", include("quickstartup.pages.urls", namespace="qs_pages")),
)
