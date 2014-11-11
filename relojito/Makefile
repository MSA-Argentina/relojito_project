BASE_SETTINGS := relojito.settings.base
LOCAL_SETTINGS := relojito.settings.development
STAGING_SETTINGS := relojito.settings.staging
PRODUCTION_SETTINGS := relojito.settings.production

AXES_RESET := axes_reset --settings=$(LOCAL_SETTINGS)
COMPILEMESSAGES := compilemessages --settings=$(LOCAL_SETTINGS)
CONSOLE := shell --settings=$(LOCAL_SETTINGS)
CONSOLE_PLUS := shell_plus --settings=$(LOCAL_SETTINGS)
DBSHELL := dbshell --settings=$(LOCAL_SETTINGS)
LOCALSERVER := runserver --settings=$(LOCAL_SETTINGS)
LOCALSERVER_PLUS := runserver_plus --settings=$(LOCAL_SETTINGS)
MAKEMIGRATION := makemigrations --settings=$(LOCAL_SETTINGS) --noinput
MESSAGES := makemessages --all --settings=$(LOCAL_SETTINGS)
MIGRATE := migrate --settings=$(LOCAL_SETTINGS) --noinput
SUPERUSER := createsuperuser --settings=$(LOCAL_SETTINGS)

.PHONY: run syncdb createsuperuser shell shell_plus

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

notebook:
		@echo 'Starting shell_plus (IPython notebook)'
		@python manage.py $(CONSOLE_PLUS) --notebook

dbshell:
		@echo 'Starting DB console'
		@python manage.py $(DBSHELL)

axes_reset:
		@echo 'Resetting lockouts...'
		@python manage.py $(AXES_RESET)

messages:
		@echo 'Preparing strings to translate...'
		@python manage.py $(MESSAGES)

compilemessages:
		@echo 'Compiling messages...'
		@python manage.py $(COMPILEMESSAGES)
