# Quickstartup

## Requirements

- Python 2.7 or newer
- virtualenv
- pip

## Starting a new project

To start a new project you'll need to install all project requirements and follow the steps bellow.

### Create a new and clone repository

Replace `myproject` with the project's repository name.

```
$ mkdir myproject
$ cd myproject
$ virtualenv .venv
$ git clone https://github.com/osantana/quickstartup.git myproject
```

### Bootstrap new project

Now you need to run the bootstrap script that will ask you some questions about the project that you will start:

```
$ myproject/bootstrap.py
```

You can call `bootstrap.py` passing the answers as arguments to script. Show arguments available:

```
$ myproject/bootstrap.py --help
```
