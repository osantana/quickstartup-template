# coding: utf-8


from django.conf import settings


def project_infos(request):
    return {
        "PROJECT_NAME": settings.PROJECT_NAME,
        "PROJECT_DOMAIN": settings.PROJECT_DOMAIN,
        "PROJECT_COPYRIGHT": settings.PROJECT_COPYRIGHT,
        "PROJECT_LICENSE": settings.PROJECT_LICENSE,
        "PROJECT_ADDRESS": settings.PROJECT_ADDRESS,
    }
