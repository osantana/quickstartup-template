# coding: utf-8


from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # QUICKSTARTUP: Replace the url mapping bellow with your application urls module
    url("^", include("apps.sample.urls")),

    # Django Admin Interface
    url(r"^admin/", include(admin.site.urls)),

    # This url must be the last one
    url(r"^accounts/", include("quickstartup.users.urls")),
    url(r"^", include("quickstartup.website.urls")),
)
