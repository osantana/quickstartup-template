deps:
	pip install -r requirements/local.txt

setup: deps

makemessages:
	python manage.py makemessages -l pt_BR

%:
	python manage.py $@ --settings=django_quickstartup.settings.local $(ARGS)
