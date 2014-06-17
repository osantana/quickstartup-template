# coding: utf-8


from django.conf import settings


def project_infos(request):
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
        "PROJECT_DOMAIN": settings.PROJECT_DOMAIN,
        "PROJECT_CONTACT": settings.PROJECT_CONTACT,
    }


def project_settings(request):
    return {"PROJECT_SETTINGS": settings}
