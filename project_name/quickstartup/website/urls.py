# coding: utf-8


from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r"^$", "quickstartup.website.views.index", name="index"),
)
