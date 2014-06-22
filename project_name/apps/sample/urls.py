# coding: utf-8


from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r"^app/$", "apps.sample.views.home", name="index"),
)
