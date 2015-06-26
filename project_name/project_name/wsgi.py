#!/usr/bin/env python

import os
from pathlib import Path

from quickstartup.settings_utils import get_project_package


PROJECT_DIR = Path(__file__).absolute().parents[1]
PROJECT_PACKAGE = get_project_package(PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(PROJECT_PACKAGE))

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()


try:
    from dj_static import MediaCling
    _application = MediaCling(_application)
except ImportError:
    pass


try:
    from dj_static import Cling
    _application = Cling(_application)
except ImportError:
    pass


def application(environ, start_response):
    # Copy all QS_* wsgi environments to os.environ removing QS_ prefix
    # This is useful to use Apache SetEnv option to pass configuration
    # arguments to application.
    for envvar in environ:
        if envvar.startswith("QS_"):
            os.environ[envvar[3:]] = environ[envvar]

    return _application(environ, start_response)
