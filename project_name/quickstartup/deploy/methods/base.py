# coding: utf-8


class BaseDeployer(object):
    name = "undefined"

    def setup(self, **kwargs):
        raise NotImplementedError()

    def deploy(self, **kwargs):
        raise NotImplementedError()
