#!/usr/bin/env python


import os
import sys
from pathlib import Path

from quickstartup.settings_utils import get_project_package


PROJECT_DIR = Path(__file__).absolute().parents[1]
PROJECT_PACKAGE = get_project_package(PROJECT_DIR)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(PROJECT_PACKAGE))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
