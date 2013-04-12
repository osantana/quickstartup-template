# coding: utf-8

from .project import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR.parent.child("app-messages")