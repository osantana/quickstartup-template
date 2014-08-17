# coding: utf-8


from fabric.utils import abort

from methods import linode


DEPLOY_METHODS = {
    "linode": linode,
}


def get_deployer(method_name):
    try:
        module = DEPLOY_METHODS[method_name]
    except KeyError:
        abort("Unknown deploy method: {}. Available: {}".format(method_name, ", ".join(DEPLOY_METHODS.keys())))
        return

    return module.Deployer()
