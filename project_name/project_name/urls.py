# coding: utf-8


from django.conf.urls import patterns, include, url


urlpatterns = [
    url(r"^", include("apps.sample.urls", namespace="app")),

    # Quickstartup: This url mapping must be the last one
    url(r"^", include("quickstartup.urls")),
]
