# Quickstartup

## Requirements

- Python 3.4 or newer
- pip

### Recommended

- PostgreSQL 9.3 or newer (installed and running at localhost)

## Starting a new project

```bash
$ cd directory/of/PROJECT
$ virtualenv-3.4 --no-site-packages PROJECT
$ pip3 install django
$ django-admin.py startproject --template=https://github.com/osantana/quickstartup/archive/master.zip PROJECT
```

## Database configuration

* Create a role with permissions to create databases on your local PostgreSQL
* Create a database to use during your development

## Basic configuration

```bash
# PROJECT/.env
DEBUG=True
LOG_LEVEL=DEBUG
PROJECT_DOMAIN=localhost:8000
SECRET_KEY=SUPER-SEKRET
# Put your postgresql credentials and database below
DATABASE_URL=postgresql://PROJECT:PROJECT@localhost/PROJECT
EMAIL_URL=file:///tmp/email-messages
```
