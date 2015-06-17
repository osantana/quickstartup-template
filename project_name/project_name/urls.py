# coding: utf-8


from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    '',  # prefix

    # QUICKSTARTUP: Replace the url mapping bellow with your application urls module
    url(r"^", include("apps.sample.urls", namespace="app")),

    # Django Admin Interface
    url(r"^admin/", include(admin.site.urls)),

    # This url mappings must be the last one
    url(r"^", include("quickstartup.urls")),
)
