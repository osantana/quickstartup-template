# coding: utf-8


from .production import *


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = str(BASE_DIR["app-messages"])

TIME_ZONE = "America/Sao_Paulo"
PROJECT_DOMAIN = "localhost:8000"

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS += (
    'debug_toolbar',
)
