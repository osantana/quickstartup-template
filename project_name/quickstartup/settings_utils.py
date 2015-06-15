# coding: utf-8
#
# Extract heavy logic from settings.py, manage.py and wsgi.py
#


import logging


class CustomAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        messages = []
        data = kwargs.get('extra', {})
        for key, value in sorted(data.items()):
            if "pass" in key:
                value = '*' * 6

            messages.append('{}={!r}'.format(key, value))
        return '{} {}'.format(msg, ', '.join(messages)), kwargs


def get_logger(name):
    return CustomAdapter(logging.getLogger(name), {})


def get_loggers(level, loggers):
    logging.addLevelName('DISABLED', logging.CRITICAL + 10)

    log_config = {
        'handlers': ['console'],
        'level': level,
    }

    if level == 'DISABLED':
        loggers = {'': {'handlers': ['null'], 'level': 'DEBUG', 'propagate': False}}
    else:
        loggers = {logger.strip(): log_config for logger in loggers}

    return loggers


def get_project_package(base_dir):
    if (base_dir / "project_name").exists():
        project_name = "project_name"
    else:
        project_name = "{{ project_name }}"  # rendered by django-admin.py startproject

    return project_name


def get_site_id(domain, name):
    from django.contrib.sites.models import Site
    from django.db import ProgrammingError
    try:
        site = Site.objects.get(pk=1)
    except Site.DoesNotExist:
        site = Site.objects.create(domain=domain, name=name)
    except ProgrammingError:
        return 1

    site.domain = domain
    site.name = name
    site.save()

    return site.id


def get_static_root(base_dir):
    try:
        from dj_static import Cling
    except ImportError:
        return str(base_dir / "static")

    return "staticfiles"


def get_media_root(base_dir):
    try:
        from dj_static import MediaCling
    except ImportError:
        return str(base_dir / "media")

    return "media"
