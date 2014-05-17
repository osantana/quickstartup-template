#!/usr/bin/env python
# coding: utf-8
"""Assume an activated virtualenv."""

from __future__ import print_function, unicode_literals

import argparse
import codecs
import fnmatch
import os
import random
import re
import sys

import pip


DEPLOYMENT_METHODS = (
    'webfaction',
    'heroku',
    'digital_ocean',
    'linode',
    'aws',
)

PY3 = sys.version[0] == 3
BASE_PATH = os.path.realpath(os.path.dirname(__file__))
PLACEHOLDER_CONTENT = re.compile(r'^(\s*).*# BOOTSTRAP: *(.*)$')
PLACEHOLDER_NAME = "project_name"
SECRET_KEY_SIZE = 50
DB_USERNAME_SIZE = 15
DB_PASSWORD_SIZE = 15
DEFAULT_PROJECT_NAME = "Quickstartup"
DEFAULT_DOMAIN = "quickstartup.us"
DEFAULT_CONTACT = "contact@quickstartup.us"
REQUIREMENTS = [
    "Fabric==1.8.3",
]
IGNORE_LIST = (
    "bootstrap.py",
    "*.py[co]",
    "*.png",
    "*.jpg",
    "*.gif",
    "*.ttf",
    "*.eot",
    "*.woff",
)

if not PY3:
    input = raw_input


def validate_email(value):
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*$"
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"$)',
        re.IGNORECASE)
    domain_regex = re.compile(r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})$',
                              re.IGNORECASE)
    domain_whitelist = ['localhost']

    if not value or '@' not in value:
        raise ValueError("Invalid email.")

    user_part, domain_part = value.rsplit('@', 1)

    if not user_regex.match(user_part):
        raise ValueError("Invalid email.")

    if domain_part not in domain_whitelist and not domain_regex.match(domain_part):
        raise ValueError("Invalid email.")

    return value


def project_name(value):
    if re.search(r'^[_a-zA-Z]\w*$', value):
        return value

    if not re.search(r'^[_a-zA-Z]', value):
        message = 'make sure the name begins with a letter or underscore'
    else:
        message = 'use only numbers, letters and underscores'

    raise ValueError("%r is not a valid name. Please %s." % (value, message))


def ask(question, options=None, default=None, validator=lambda v: v):
    if options:
        question = "%s: %s? " % (question, ", ".join(options))
    else:
        question = "%s? " % (question,)

    if default:
        question = "%s[%s] " % (question, default)

    while True:
        try:
            value = input(question).strip()
            if not value:
                value = default
            value = validator(value)
        except EOFError:
            print()
            sys.exit(2)
        except ValueError, ex:
            print("ERROR:", ex)
            continue

        if options and value not in options:
            continue

        if value:
            return value


def _execute_local_setup():
    from fabric.tasks import execute
    from fabfile.local import local_setup
    execute(local_setup)

def setup(echo):
    os.chdir(BASE_PATH)

    print("Installing Fabric for local setup and deployments...")
    error = pip.main(["--quiet", "install", "--upgrade"] + REQUIREMENTS)
    if error:
        echo("Cannot install {}".format(", ".join(REQUIREMENTS)))

    print("Setup local environment...")
    _execute_local_setup()


def generate_random_string(size, symbols=True):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if symbols:
        allowed_chars += "!@#$%^&*(-_=+)"
    return "".join(random.choice(allowed_chars) for _ in range(size))


def create_secret_key():
    return generate_random_string(SECRET_KEY_SIZE)


def create_db_username():
    return generate_random_string(DB_USERNAME_SIZE, symbols=False)


def create_db_password():
    return generate_random_string(DB_PASSWORD_SIZE, symbols=False)


def render(path, context):
    try:
        with codecs.open(path, encoding="utf-8") as infile:
            content = infile.readlines()
    except (IOError, UnicodeError, OSError), ex:
        print("Error reading {} ({})".format(path, ex))
        return

    for i, line in enumerate(content):
        if not PLACEHOLDER_CONTENT.match(line):
            continue

        for variable in context:
            content[i] = content[i].replace("@@{}@@".format(variable), context[variable])

        content[i] = PLACEHOLDER_CONTENT.sub(r'\1\2', content[i])

    with codecs.open(re.sub(r".local$", "", path), mode="w", encoding="utf-8") as outfile:
        outfile.writelines(content)


def create_project(name, deploy_method, project, domain, contact):
    context = {
        'name': name,
        'deploy_method': deploy_method,
        'project': project,
        'domain': domain,
        'contact': contact,
        'secret_key': create_secret_key(),
        'db_username': create_db_username(),
        'db_password': create_db_password(),
    }

    for root, directories, files in os.walk(BASE_PATH):
        if ".git" in directories:
            directories.remove(".git")

        for i, directory in enumerate(directories):
            if PLACEHOLDER_NAME not in directory:
                continue

            new_name = directory.replace(PLACEHOLDER_NAME, name)
            os.rename(os.path.join(root, directory), os.path.join(root, new_name))
            directories[i] = new_name

        for i, filename in enumerate(files):
            if any(fnmatch.fnmatch(filename, pattern) for pattern in IGNORE_LIST):
                print("Skipping {}...".format(filename))
                continue

            if PLACEHOLDER_NAME in filename:
                new_name = filename.replace(PLACEHOLDER_NAME, name)
                os.rename(os.path.join(root, filename), os.path.join(root, new_name))
                files[i] = new_name

            render(os.path.join(root, files[i]), context)

    return context


def main():
    parser = argparse.ArgumentParser(description='Bootstrap Quickstartup Project')
    parser.add_argument("-s", "--skip-setup", action="store_true", help="skip local environment setup.")
    parser.add_argument("-n", "--name", nargs="?")
    parser.add_argument("-m", "--deploy-method", nargs="?")
    parser.add_argument("-p", "--project", nargs="?")
    parser.add_argument("-d", "--domain", nargs="?")
    parser.add_argument("-c", "--contact", nargs="?")
    args = parser.parse_args()

    default_name = os.path.basename(BASE_PATH)
    if default_name == "quickstartup":
        default_name = "myproject"

    if not args.name:
        args.name = ask("What is the project name", default=default_name, validator=project_name)

    if not args.deploy_method:
        args.deploy_method = ask("What is the deploy method",
                                 default=DEPLOYMENT_METHODS[0], options=DEPLOYMENT_METHODS,
                                 validator=lambda x: x.lower())

    if not args.project:
        args.project = ask("What is the project name", default=DEFAULT_PROJECT_NAME)

    if not args.domain:
        args.domain = ask("What is the project domain", default=DEFAULT_DOMAIN)

    if not args.contact:
        args.contact = ask("What is the contact email", default=DEFAULT_CONTACT, validator=validate_email)

    if not args.skip_setup:
        setup(parser.error)

    context = create_project(name=args.name, deploy_method=args.deploy_method,
                             project=args.project, domain=args.domain, contact=args.contact)

    print("⚠️  Create a database {name} in your local PostgreSQL server.".format(**context))
    print("⚠️  Make database {name} with admin permissions for credentials:\n".format(**context))

    print("    Username: {db_username}".format(**context))
    print("    Password: {db_password}\n".format(**context))

    print("⚠️  You can change these connection information in your .env file on project root.\n\n")


if __name__ == "__main__":
    main()

