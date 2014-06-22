# coding: utf-8


from fabric.api import local
from fabric.decorators import task


@task
def local_setup():
    local("pip install -U -r requirements/local.txt")
