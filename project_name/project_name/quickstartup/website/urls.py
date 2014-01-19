# coding: utf-8


from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r"^$", "quickstartup.website.views.homepage", name="homepage"),
    url(r"^contact/$", "quickstartup.website.views.contact", name="contact"),
    url(r"^(?P<url>.*)$", "quickstartup.website.views.website_page", name="page"),
)
