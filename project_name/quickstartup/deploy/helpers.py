# coding: utf-8

import os
import shutil
import random
import string

from fabric.operations import local
from fabric.colors import green, blue, yellow, white, red


def gen_random_string(size):
    return "".join(random.choice(string.letters + string.digits) for x in range(size))


def get_key_from_file(filename):
    try:
        with open(os.path.expanduser(filename)) as keyfile:
            return keyfile.read()
    except IOError:
        return


def create_rsa_keypair(public):
    public = os.path.expanduser(public)
    private, ext = os.path.splitext(public)

    if ext != ".pub":
        return

    if os.path.isfile(public):
        shutil.copy(public, public + ".bak")

    if os.path.isfile(private):
        shutil.copy(private, private + ".bak")

    local('echo "y" | ssh-keygen -b 2048 -t rsa -f {} -q -N ""'.format(private), capture=True)

    return private, public


def print_header(deploy_method_name, step):
    print "=" * 72
    print blue("Quickstartup Deployment System"), "(c) osantana"
    print "=" * 72
    print
    print "  •", green("Method:"), deploy_method_name
    print "  •", green("Step:  "), step
    print


def print_help(title, doc):
    help_message = []

    indentation = None
    size = 0
    for line in doc.splitlines():
        if indentation is None:
            striped = line.lstrip()
            indentation = len(line) - len(striped)
        line = line[indentation:]
        size = max(len(line), size)
        help_message.append(line)

    center = (size - len(title)) / 2

    print yellow("=" * center), white(title, bold=True), yellow("=" * center)
    print
    print white("\n".join(help_message), bold=False)
    print
    print yellow("=" * (2 * center + len(title) + 2))
    print


def print_step(step):
    print "  •", red("Next Step:"), step, "(fab -ak {})".format(step)
