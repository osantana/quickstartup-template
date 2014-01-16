#!/usr/bin/env python


import os
import argparse
import shutil
import json
import codecs
import re

from binaryornot.check import is_binary


COOKIECUTTER_REPO = "git@github.com:osantana/cookiecutter-quickstartup.git"
QUOTED = '''["']%s["']'''
CHANGELOG_HEADER = """# Changelog

"""
LOG_FORMAT = "* [view commit](http://github.com/osantana/cookiecutter-quickstartup/commit/%H) %s"

RAW_FILES_EXT = (
    ".html",
)


def clone(target):
    if not os.path.isdir(os.path.join(target, ".git")):
        shutil.rmtree(target)
        os.system("git clone {repo} {dir}".format(repo=COOKIECUTTER_REPO, dir=target))

    for filename in os.listdir(target):
        if filename == ".git":
            continue

        path = os.path.join(target, filename)

        if os.path.isdir(path):
            shutil.rmtree(os.path.join(target, filename))
        else:
            os.remove(path)


def export(target):
    os.system("git archive master | tar -x -C {dir}".format(dir=target))


def generate_changelog(target):
    changelog = os.path.join(target, "Changelog.md")
    cmd = 'git log --pretty=format:"%s"' % LOG_FORMAT
    with open(changelog, "w") as log:
        log.write(CHANGELOG_HEADER)
    os.system("{cmd} >> {changelog}".format(cmd=cmd, changelog=changelog))


def load_settings(target):
    with open(os.path.join(target, "cookiecutter.json")) as settings_file:
        settings = json.load(settings_file)
    return {v: "{{cookiecutter.%s}}" % (k,) for k, v in settings.iteritems()}


def generate_cookiecutter(target, settings):
    for path, dirs, files in os.walk(target):
        if ".git" in path:
            continue

        for i, basename in enumerate(dirs):
            dirname = os.path.join(path, basename)

            if basename in settings:
                os.rename(dirname, os.path.join(path, settings[basename]))
                dirs[i] = settings[basename]

        for basename in files:
            filename = os.path.join(path, basename)

            if is_binary(filename) or basename == "cookiecutter.json":
                continue

            source = codecs.open(filename, encoding="utf-8").readlines()

            if not source:
                continue

            target = []
            for line in source:
                for key, value in settings.iteritems():
                    line = re.sub(QUOTED % (key,), '"%s"' % (value,), line)
                target.append(line)

            ext = os.path.splitext(filename)[-1]
            if ext in RAW_FILES_EXT:
                target[0] = "{% raw %}" + target[0]
                target[-1] += "{% endraw %}"

            with codecs.open(filename, "w", encoding="utf-8") as filehandler:
                filehandler.writelines(target)


def main():
    parser = argparse.ArgumentParser(description="Generate/Update cookiecutter repository")
    parser.add_argument('target')
    args = parser.parse_args()

    target = os.path.abspath(args.target)

    clone(target)
    export(target)
    settings = load_settings(target)
    generate_cookiecutter(target, settings)
    generate_changelog(target)
    # TODO: commit with changelog message & push (?)

if __name__ == "__main__":
    main()
