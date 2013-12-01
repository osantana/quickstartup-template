# coding: utf-8


from django.utils.translation import ugettext_lazy as _

from pathlib import Path
from decouple import config
from dj_database_url import parse as parse_db_url


BASE_DIR = Path(__file__).parent(3)
FRONTEND_DIR = BASE_DIR["frontend"]


# Project Info
PROJECT_NAME = "{{cookiecutter.project_name}}"
PROJECT_DOMAIN = "djangoquickstartup.io"
PROJECT_COPYRIGHT = "2013 Osvaldo Santana Neto"
PROJECT_LICENSE = _("MIT License")
PROJECT_CONTACT = "contact@djangoquickstartup.io"
PROJECT_ADDRESS = """<strong>Django Quickstartup Co.</strong><br>
  0 Dumb Street<br>
  Brazil<br>
  <abbr title="Phone">P:</abbr> (123) 456-7890
"""

# Debug & Development
DEBUG = config("DEBUG", default=False, cast=bool)
TEMPLATE_DEBUG = config("TEMPLATE_DEBUG", default=DEBUG, cast=bool)


# Database
DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
        cast=parse_db_url
    )
}


# Email
DEFAULT_FROM_EMAIL = PROJECT_CONTACT
DEFAULT_TRANSACTIONAL_EMAIL = {
    "contact": True,
}

# Security & Authentication
ALLOWED_HOSTS = []
SECRET_KEY = config("SECRET_KEY")
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGIN_URL = "/accounts/signin/"
ACCOUNT_ACTIVATION_DAYS = 7


# i18n & l10n
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("en", u"English"),
    ("pt-br", u"Português (Brasil)"),
)

LOCALE_PATHS = (
    str(BASE_DIR["locale"]),
)


# Miscelaneous
ROOT_URLCONF = "project_name.urls"
WSGI_APPLICATION = "project_name.wsgi.application"


# Media & Static
MEDIA_URL = "/media/"
MEDIA_ROOT = str(FRONTEND_DIR["media"])    # FIXME: Deployment config

STATIC_URL = "/static/"
STATICFILES_DIRS = (
    str(FRONTEND_DIR["static"]),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Template
TEMPLATE_DIRS = (
    str(FRONTEND_DIR["templates"]),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "quickstartup.commons.context_processors.project_infos",
)


# Application
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party libs
    'south',
    'django_extensions',

    # Quick Startup Apps
    'quickstartup.commons',
    'quickstartup.users',
    'quickstartup.website',

    # QUICKSTARTUP: Your apps, you can replace the sample aplication bellow with your app
    'apps.sample',
)
