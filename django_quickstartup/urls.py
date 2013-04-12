# coding: utf-8


from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^admin/", include(admin.site.urls)),

    # Replace URL below with your application urls.py
    # url("^app/", include("django_quickstartup.your_app.urls")),

    url(r"^", include("django_quickstartup.quickstartup.urls")),
)
