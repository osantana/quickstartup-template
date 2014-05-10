# coding: utf-8

from django.http import Http404

from django.conf import settings

from .views import website_page


class WebsitePageMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response

        try:
            return website_page(request, request.path_info)
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response
