# coding: utf-8


from pathlib import Path

from django.test import TestCase


TEST_ROOT_DIR = Path(__file__).parent


class BaseTestCase(TestCase):
    pass
