# coding: utf-8
#
# TODO: Replace this module with envconfig project https://github.com/osantana/envconfig


import os


from django.core.exceptions import ImproperlyConfigured

import dj_database_url
from pathlib import Path


def get_env_setting(key, default=None):
    key = "DJANGO_" + key.upper()

    if key not in os.environ and default is None:
        raise ImproperlyConfigured("Undefined %s environment variable." % (key,))

    config = os.environ.get(key, default)

    if isinstance(config, str) and config.lower() in ("true", "false"):
        return config.lower() == "true"

    return config


def get_project_directory(path):
    base_dir = Path(path).parent(3)
    frontend_dir = base_dir["frontend"]
    return base_dir, frontend_dir


def get_database_settings(base_dir):
    try:
        url = os.environ["DATABASE_URL"]
    except KeyError:
        raise ImproperlyConfigured("Undefined DATABASE_URL environment variable.")

    config = dj_database_url.parse(url)

    # handle local development settings
    if config["ENGINE"] == "django.db.backends.sqlite3":
        config["NAME"] = config["NAME"].replace("[BASE_DIR]", str(base_dir))

    return {'default': config}
