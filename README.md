# Quickstartup

## Requirements

- Python 3.7 or newer
- pip

### Recommended

- PostgreSQL 9.3 or newer (installed and running at localhost)

## Starting a new project

```bash
$ cd directory/of/PROJECT
$ virtualenv --no-site-packages PROJECT
$ pip3 install django
$ django-admin.py startproject --template=https://github.com/osantana/quickstartup-template/archive/master.zip PROJECT
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


## Basic installation

```bash
$ pip install -r requirements-local.txt
$ cd PROJECT
$ chmod +x manage.py
$ ./manage.py migrate
```

```python
# PROJECT/settings.py

# EDIT and change the following settings:
PROJECT_NAME="My Personal Project"
PROJECT_CONTACT="contact@personal_project.com"
```


## Running

```bash
$ ./manage.py runserver
```

## It Worked!

http://localhost:8000/
## Review
#It is working fine and It is helpfull.
#Bro plz don't remove this pull request .
