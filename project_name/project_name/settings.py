# coding: utf-8


from pathlib import Path

from prettyconf import config
from dj_database_url import parse as parse_db_url
from dj_email_url import parse as parse_email_url

from quickstartup.settings_utils import (get_project_package, get_loggers,
                                         get_site_id, get_static_root, get_media_root)


# Project Structure
BASE_DIR = Path(__file__).absolute().parents[2]
PROJECT_DIR = Path(__file__).absolute().parents[1]
FRONTEND_DIR = PROJECT_DIR / "frontend"


# Project Info
PROJECT_NAME = "Django Quickstartup"
PROJECT_CONTACT = "contact@quickstartup.us"
PROJECT_DOMAIN = config("PROJECT_DOMAIN")


# Debug & Development
DEBUG = config("DEBUG", default=False, cast=config.boolean)


# Database
DATABASES = {
    'default': config('DATABASE_URL', cast=parse_db_url),
}
DATABASES['default']['CONN_MAX_AGE'] = None  # always connected


# Email
_email_config = config("EMAIL_URL", cast=parse_email_url)
EMAIL_FILE_PATH = _email_config['EMAIL_FILE_PATH']
EMAIL_HOST_USER = _email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = _email_config['EMAIL_HOST_PASSWORD']
EMAIL_HOST = _email_config['EMAIL_HOST']
EMAIL_PORT = _email_config['EMAIL_PORT']
EMAIL_BACKEND = _email_config['EMAIL_BACKEND']
EMAIL_USE_TLS = _email_config['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = PROJECT_CONTACT


# Security & Signup/Signin
ALLOWED_HOSTS = ["*"]
SECRET_KEY = config("SECRET_KEY")

AUTH_USER_MODEL = "accounts.User"
REGISTRATION_FORM = "quickstartup.accounts.forms.SignupForm"
PROFILE_FORM = "quickstartup.accounts.forms.ProfileForm"

LOGIN_URL = "qs_accounts:signin"
LOGIN_REDIRECT_URL = "app:index"
ADMIN_URL = "admin"  # empty to disable admin URLs

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in.
REGISTRATION_OPEN = True

PASSWORD_HASHERS = (
    # Set PASSWORD_HASHER=UnsaltedMD5PasswordHasher to make test running faster
    'django.contrib.auth.hashers.' + config("PASSWORD_HASHER", default="PBKDF2PasswordHasher"),
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


# Social
SOCIAL_AUTH_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_LOGIN_ERROR_URL = '/accounts/social-auth-errors/'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email']  # If user already exists, do not override his email

# SOCIAL_AUTH_TWITTER_KEY = ''
# SOCIAL_AUTH_TWITTER_SECRET = ''
# SOCIAL_AUTH_GOOGLE_OAUTH_KEY = ''
# SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = ''

AUTHENTICATION_BACKENDS = (
    # 'social.backends.twitter.TwitterOAuth',
    # 'social.backends.google.GoogleOAuth',
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
_project_package = get_project_package(PROJECT_DIR)
ROOT_URLCONF = "{}.urls".format(_project_package)
WSGI_APPLICATION = "{}.wsgi.application".format(_project_package)
SITE_ID = get_site_id(PROJECT_DOMAIN, PROJECT_NAME)


# Media & Static
MEDIA_URL = "/media/"
MEDIA_ROOT = get_media_root(BASE_DIR)

STATIC_URL = "/static/"
STATIC_ROOT = get_static_root(BASE_DIR)
STATICFILES_DIRS = (
    str(FRONTEND_DIR / "static"),
)


# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            str(FRONTEND_DIR / "templates"),
        ),
        'OPTIONS': {
            'debug': config("TEMPLATE_DEBUG", default=DEBUG, cast=config.boolean),
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'quickstartup.template_loader.Loader'
            ),
            'context_processors': (
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
            ),
        },
    },
]


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
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'quickstartup.website.middleware.WebsitePageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # 3rd party libs
    'django_extensions',
    'widget_tweaks',
    'registration',
    'social.apps.django_app.default',

    # Quick Startup Apps
    'quickstartup.core',
    'quickstartup.accounts',
    'quickstartup.website',
    'quickstartup.contacts',

    # QUICKSTARTUP: Your apps, you can replace the sample aplication bellow with your app
    'apps.sample',
)


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': get_loggers(config("LOG_LEVEL", default="INFO"),
                           config("LOGGERS", default="", cast=config.list)),
}
