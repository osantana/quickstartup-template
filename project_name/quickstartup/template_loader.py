# coding: utf-8


from pathlib import Path

from django.template.loaders.app_directories import Loader as DjangoLoader
from django.template.utils import get_app_template_dirs


QUICKSTARTUP_PATH = Path(__file__).parent


def is_quickstartup(path):
    try:
        Path(path).relative_to(QUICKSTARTUP_PATH)
    except ValueError:
        return 1
    return 0


class Loader(DjangoLoader):
    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = list(get_app_template_dirs('templates'))
            template_dirs.sort(key=is_quickstartup)

        return super().get_template_sources(template_name, template_dirs=template_dirs)
