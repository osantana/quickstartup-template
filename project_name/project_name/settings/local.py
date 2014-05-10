# coding: utf-8


from .production import *


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = str(BASE_DIR / "app-messages")

TIME_ZONE = "America/Sao_Paulo"
PROJECT_DOMAIN = "localhost:8000"

# Make test running fast
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
