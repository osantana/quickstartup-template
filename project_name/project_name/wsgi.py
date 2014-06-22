#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings.production")  # BOOTSTRAP: os.environ.setdefault("DJANGO_SETTINGS_MODULE", "@@name@@.settings.production")

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()


def application(environ, start_response):

    # Copy all QS_* wsgi environments to os.environ removing QS_ prefix
    # This is useful to use Apache SetEnv option to pass configuration
    # arguments to application.
    for envvar in environ:
        if envvar.startswith("QS_"):
            os.environ[envvar[3:]] = environ[envvar]

    return _application(environ, start_response)
