# Quickstartup

## Requirements

- Python 2.7 or newer
- virtualenv
- pip
- virtualenvwrapper (recommended)
- autoenv (recommended)
- node.js (for frontend development)

## Starting a new project

- Create a new project virtualenv

```shell
mkproject myproject  # mkproject is a virtualenvwrapper alias
```

This will auto-activate `myproject` virtualenv. Make sure that this virtualenv
is enabled when developing your project.

- Install cookiecooter

```shell
pip install cookiecutter
```

- Start a new project environment

```shell
cookiecutter https://github.com/osantana/cookiecutter-quickstartup.git
```

Cookiecutter will ask you some questions regarding your project and will use
these informations to initialize your project data.

You can answer the value of these answers in the future.

