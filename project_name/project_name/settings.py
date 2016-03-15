# coding: utf-8


from pathlib import Path

from dj_database_url import parse as parse_db_url
from dj_email_url import parse as parse_email_url
from django.contrib.messages import constants as message_constants
from prettyconf import config
from quickstartup import settings_utils


# Project Structure
BASE_DIR = Path(__file__).absolute().parents[2]
PROJECT_DIR = Path(__file__).absolute().parents[1]
FRONTEND_DIR = PROJECT_DIR / "frontend"


# Project Info
QS_PROJECT_NAME = "Django Quickstartup"
QS_PROJECT_DOMAIN = config("PROJECT_DOMAIN")
QS_PROJECT_CONTACT = "contact@{}".format(QS_PROJECT_DOMAIN)
QS_PROJECT_URL = "http://{}".format(QS_PROJECT_DOMAIN)


# Debug & Development
DEBUG = config("DEBUG", default=False, cast=config.boolean)


# Database
DATABASES = {
    'default': config('DATABASE_URL', cast=parse_db_url),
}
DATABASES['default']['CONN_MAX_AGE'] = None  # always connected


# Email
_email_config = config("EMAIL_URL", cast=parse_email_url)
_email_password = config("EMAIL_PASSWORD", default=_email_config["EMAIL_HOST_PASSWORD"])
DEFAULT_FROM_EMAIL = QS_PROJECT_CONTACT
EMAIL_BACKEND = "djmail.backends.default.EmailBackend"
EMAIL_FILE_PATH = _email_config['EMAIL_FILE_PATH']
EMAIL_HOST_USER = _email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = _email_password
EMAIL_HOST = _email_config['EMAIL_HOST']
EMAIL_PORT = _email_config['EMAIL_PORT']
EMAIL_USE_TLS = _email_config['EMAIL_USE_TLS']
DJMAIL_REAL_BACKEND = _email_config['EMAIL_BACKEND']


# Security & Signup/Signin
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=config.list, default="*")
SECRET_KEY = config("SECRET_KEY")
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
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_PASSWORD_VALIDATORS = (
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
)


# Custom User & Profile Settings
AUTH_USER_MODEL = "qs_accounts.User"
LOGIN_REDIRECT_URL = "app:index"
LOGIN_URL = "qs_accounts:signin"
QS_SIGNUP_AUTO_LOGIN = True
QS_SIGNUP_OPEN = True
QS_SIGNUP_TOKEN_EXPIRATION_DAYS = 7
QS_SIGNUP_FORM = "quickstartup.qs_accounts.forms.SignupForm"
QS_PROFILE_FORM = "quickstartup.qs_accounts.forms.ProfileForm"
QS_PASSWORD_CHANGE_FORM = 'quickstartup.qs_accounts.forms.PasswordChangeForm'
QS_ADMIN_URL = "admin"  # empty to disable admin URLs


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
_project_package = settings_utils.get_project_package(PROJECT_DIR)
ROOT_URLCONF = "{}.urls".format(_project_package)
WSGI_APPLICATION = "{}.wsgi.application".format(_project_package)
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}


# Media & Static
MEDIA_URL = "/media/"
MEDIA_ROOT = settings_utils.get_media_root(BASE_DIR)

STATIC_URL = "/static/"
STATIC_ROOT = settings_utils.get_static_root(BASE_DIR)
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
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "quickstartup.context_processors.project_infos",
                "quickstartup.context_processors.project_settings",
            ),
        },
    },
]


# Applications
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'quickstartup.qs_website.middleware.WebsitePageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party libs
    'django_extensions',
    'widget_tweaks',
    'djmail',

    # Quick Startup Apps
    'quickstartup.qs_core',
    'quickstartup.qs_accounts',
    'quickstartup.qs_website',
    'quickstartup.qs_contacts',

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
    'loggers': settings_utils.get_loggers(config("LOG_LEVEL", default="INFO"),
                                          config("LOGGERS", default="", cast=config.list)),
}
