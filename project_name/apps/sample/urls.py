# coding: utf-8


from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r"^dashboard/$", "apps.sample.views.dashboard", name="app-dashboard"),
)
