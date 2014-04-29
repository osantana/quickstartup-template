# coding: utf-8


from fabric.api import env

from .local import *


DEPLOYMENT_METHODS = (
    'webfaction',
    'heroku',
    'digital_ocean',
    'linode',
    'aws',
)
