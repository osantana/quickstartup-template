# coding: utf-8


from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # QUICKSTARTUP: Replace the url mapping bellow with your application urls module
    url("^", include("apps.sample.urls", namespace="app")),
    # social authentication
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Django Admin Interface
    url(r"^admin/", include(admin.site.urls)),

    # This url mappings must be the last one
    url(r"^accounts/", include("quickstartup.accounts.urls", namespace="qs_accounts")),
    url(r"^contact/$", include("quickstartup.contacts.urls", namespace="qs_contacts")),
    url(r"^", include("quickstartup.website.urls", namespace="qs_pages")),
)
