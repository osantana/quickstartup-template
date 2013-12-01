#!/usr/bin/env python


import os
import sys


if __name__ == "__main__":
    if os.path.exists(os.path.join(os.path.dirname(__file__), "project_name")):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.repo_name}}.settings.production")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
