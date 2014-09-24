# coding: utf-8


from pathlib import Path
from decouple import config
from dj_database_url import parse as parse_db_url


BASE_DIR = Path(__file__).parents[3]
PROJECT_DIR = Path(__file__).parents[2]
FRONTEND_DIR = PROJECT_DIR / "frontend"


# Project Info
PROJECT_ID = "quickstartup"   # BOOTSTRAP: PROJECT_ID = "@@id@@"
PROJECT_NAME = "Django Quickstartup"  # BOOTSTRAP: PROJECT_NAME = "@@name@@"
PROJECT_DOMAIN = "quickstartup.us"  # BOOTSTRAP: PROJECT_DOMAIN = "@@domain@@"
PROJECT_CONTACT = "contact@quickstartup.us"  # BOOTSTRAP: PROJECT_CONTACT = "@@contact@@"


# Debug & Development
DEBUG = config("DEBUG", default=False, cast=bool)
TEMPLATE_DEBUG = config("TEMPLATE_DEBUG", default=DEBUG, cast=bool)


# Database
DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///%s' % ((BASE_DIR / "db.sqlite3"),),
        cast=parse_db_url
    )
}
DATABASES['default']['ATOMIC_REQUESTS'] = True  # transactions tied to request->response
DATABASES['default']['CONN_MAX_AGE'] = None  # always connected


# Email
DEFAULT_FROM_EMAIL = PROJECT_CONTACT
DEFAULT_TRANSACTIONAL_EMAIL = {
    "contact": True,
}

# Security & Authentication
ALLOWED_HOSTS = ["*"]
SECRET_KEY = config("SECRET_KEY")
AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = "/app/"
LOGIN_URL = "/accounts/signin/"
ACCOUNT_ACTIVATION_DAYS = 7
# social authentication, more at http://python-social-auth.readthedocs.org
SOCIAL_AUTH_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL
SOCIAL_AUTH_LOGIN_URL = LOGIN_REDIRECT_URL
SOCIAL_AUTH_LOGIN_ERROR_URL = LOGIN_URL
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'  # -> signout ?
SOCIAL_AUTH_INACTIVE_USER_URL = '/'  # -> signup ?
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
# This should be set properly by each backend (check the documentation)
#SOCIAL_AUTH_TWITTER_KEY = ''
#SOCIAL_AUTH_TWITTER_SECRET = ''
#SOCIAL_AUTH_GOOGLE_OAUTH_KEY = ''
#SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = ''

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
)


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
    str(PROJECT_DIR / "locale"),
)


# Miscelaneous
ROOT_URLCONF = "project_name.urls"
WSGI_APPLICATION = "project_name.wsgi.application"


# Media & Static
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "media")

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "static")
STATICFILES_DIRS = (
    str(FRONTEND_DIR / "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Template
TEMPLATE_DIRS = (
    str(FRONTEND_DIR / "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
    "quickstartup.context_processors.project_infos",
    "quickstartup.context_processors.project_settings",
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
    'django.middleware.gzip.GZipMiddleware',
    'quickstartup.website.middleware.WebsitePageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party libs
    'django_extensions',
    'widget_tweaks',
    # social authentication
    'social.apps.django_app.default',

    # Quick Startup Apps
    'quickstartup.deploy',
    'quickstartup.accounts',
    'quickstartup.website',
    'quickstartup.contacts',

    # QUICKSTARTUP: Your apps, you can replace the sample aplication bellow with your app
    'apps.sample',
)


# Deployment Settings
DEPLOY_METHOD = config("DEPLOY_METHOD", default="linode")

# TODO: check these defaults
DEPLOY_DATA = {
    "hostname": config("DEPLOY_HOSTNAME", default=PROJECT_ID),
    "server_ip": config("DEPLOY_SERVER_IP", default=PROJECT_DOMAIN),
    "username": config("DEPLOY_USERNAME", default=PROJECT_ID),
    "user_pubkey": config("DEPLOY_USER_PUBKEY", default="~/.ssh/id_rsa.pub"),
}
