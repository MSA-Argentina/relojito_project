SETTINGS := relojito.settings.$(RELOJITO_ENVIRONMENT)

COLLECTSTATIC := collectstatic --noinput --settings=$(SETTINGS)
COMPILEMESSAGES := compilemessages --settings=$(SETTINGS)
CONSOLE := shell --settings=$(SETTINGS)
CONSOLE_PLUS := shell_plus --settings=$(SETTINGS)
DBSHELL := dbshell --settings=$(SETTINGS)
LOCALSERVER := runserver --settings=$(SETTINGS)
LOCALSERVER_PLUS := runserver_plus --settings=$(SETTINGS)
MAKEMIGRATION := makemigrations --settings=$(SETTINGS) --noinput
MESSAGES := makemessages --all --settings=$(SETTINGS)
MIGRATE := migrate --settings=$(SETTINGS) --noinput
SUPERUSER := createsuperuser --settings=$(SETTINGS)

.PHONY: run createsuperuser shell shell_plus

run:
		@echo 'Running development server...'
		@python manage.py $(LOCALSERVER) 0.0.0.0:8090

run_plus:
		@echo 'Running development server_plus...'
		@python manage.py $(LOCALSERVER_PLUS) 0.0.0.0:8090

migrations:
		@echo 'Creating migrations...'
		@python manage.py $(MAKEMIGRATION)

migrate:
		@echo 'Applying migrations...'
		@python manage.py $(MIGRATE)

superuser:
		@echo 'Creating superuser'
		@python manage.py $(SUPERUSER)

shell:
		@echo 'Starting Django shell...'
		@python manage.py $(CONSOLE)

shell_plus:
		@echo 'Starting Django shell_plus...'
		@python manage.py $(CONSOLE_PLUS)

collectstatic:
		@echo 'Compiling statics...'
		@python manage.py $(COLLECTSTATIC)

notebook:
		@echo 'Starting shell_plus (IPython notebook)'
		@python manage.py $(CONSOLE_PLUS) --notebook

celery:
		@echo 'Starting celery...'
		@celery -A relojito worker -B -l info

celery_shell:
		@echo 'Starting celery shell...'
		@celery shell -A relojito

dbshell:
		@echo 'Starting DB console'
		@python manage.py $(DBSHELL)

messages:
		@echo 'Preparing strings to translate...'
		@python manage.py $(MESSAGES)

compilemessages:
		@echo 'Compiling messages...'
		@python manage.py $(COMPILEMESSAGES)
