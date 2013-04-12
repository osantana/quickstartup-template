# coding: utf-8


from unipath import Path
from django.utils.translation import ugettext_lazy as _


BASE_DIR = Path(__file__).ancestor(3)


# Project Info
PROJECT_NAME = _("Django Quickstartup")
PROJECT_DOMAIN = "djangoquickstartup.io"
PROJECT_COPYRIGHT = "2013 Osvaldo Santana Neto"
PROJECT_LICENSE = _("MIT License")
PROJECT_CONTACT = "contact@djangoquickstartup.io"
ACCOUNT_ACTIVATION_DAYS = 7

# Debug & Development
DEBUG = False
TEMPLATE_DEBUG = DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Admins & Managers
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.child("project.db"),  # TODO: use {{ project_name }}
    }
}


# Email
DEFAULT_FROM_EMAIL = PROJECT_CONTACT


# Security & Authentication
ALLOWED_HOSTS = []
SECRET_KEY = "0(q2&ku+ysx9-zi&5(-r=l6y7k)!*p4bf2jhwj7dd4+7k5m4%+"  # TODO: put in secretsrc
AUTH_USER_MODEL = "quickstartup.User"
LOGIN_REDIRECT_URL = "/app/"


# i18n & l10n
TIME_ZONE = "America/Chicago"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("en", u"English"),
    ("pt-br", u"Português (Brasil)"),
)

LOCALE_PATHS = (
    BASE_DIR.child("locale"),
)


# Miscelaneous
ROOT_URLCONF = "django_quickstartup.urls"
WSGI_APPLICATION = "django_quickstartup.wsgi.application"


# Media & Static
MEDIA_ROOT = ""  # XXX: Host-specific setting
STATIC_ROOT = ""  # XXX: Host-specific setting
MEDIA_URL = "/media/"
STATIC_URL = "/static/"

STATICFILES_DIRS = (
    BASE_DIR.child("static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Template
TEMPLATE_DIRS = (
    BASE_DIR.child("templates"),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django_quickstartup.quickstartup.context_processors.project_infos",
)


# Application
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd libs
    'south',
    'django_extensions',

    # Quick Startup Apps
    'django_quickstartup.quickstartup',

    # Your apps
    # ...
)
