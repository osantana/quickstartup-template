# coding: utf-8


from .settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR.parent.child("app-messages")

TIME_ZONE = "America/Sao_Paulo"
PROJECT_DOMAIN = "localhost:8000"