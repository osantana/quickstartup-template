# coding: utf-8


from copy import copy
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import get_deployer
from ...helpers import print_header


class Command(BaseCommand):
    help = 'Deploy project'

    option_list = BaseCommand.option_list + (
        make_option('--setup', action='store_true', dest='setup', default=False, help='Initial server setup.'),
    )

    def _get_extra_locales(self):
        extra_locales = []
        for code, name in settings.LANGUAGES:
            code = code.replace("-", "_")
            code = code[:2] + code[2:].upper()

            if code in ("en", "en_US"):
                continue

            extra_locales.append("{}.UTF-8".format(code))

        return " ".join(extra_locales)

    def handle(self, *args, **options):
        method_name = settings.DEPLOY_METHOD
        deployer = get_deployer(method_name)
        deploy_data = copy(settings.DEPLOY_DATA)

        if "setup" in options and options["setup"]:
            print_header(method_name, "setup")
            deploy_data["extra_locales"] = self._get_extra_locales()
            deployer.setup(**deploy_data)
            return

        print_header(method_name, "deploy")
        deployer.deploy(**deploy_data)
