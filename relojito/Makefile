BASE_SETTINGS := relojito.settings.base
LOCAL_SETTINGS := relojito.settings.base
STAGING_SETTINGS := relojito.settings.staging
PRODUCTION_SETTINGS := relojito.settings.production

LOCALSERVER := runserver --settings=$(LOCAL_SETTINGS)
LOCALSERVER_PLUS := runserver_plus --settings=$(LOCAL_SETTINGS)
SYNCDB := syncdb --settings=$(LOCAL_SETTINGS) --noinput
MAKEMIGRATION := makemigrations --settings=$(LOCAL_SETTINGS) --noinput
MIGRATE := migrate --settings=$(LOCAL_SETTINGS) --noinput
CREATEDB := syncdb --settings=$(LOCAL_SETTINGS) --noinput --no-initial-data
SUPERUSER := createsuperuser --settings=$(LOCAL_SETTINGS)
CONSOLE := shell --settings=$(LOCAL_SETTINGS)
CONSOLE_PLUS := shell_plus --settings=$(LOCAL_SETTINGS)
DBSHELL := dbshell --settings=$(LOCAL_SETTINGS)
MESSAGES := makemessages --all --settings=$(LOCAL_SETTINGS)
COMPILEMESSAGES := compilemessages --settings=$(LOCAL_SETTINGS)

.PHONY: run syncdb createsuperuser shell shell_plus

run:
		@echo 'Corriendo server...'
		@python manage.py $(LOCALSERVER) 0.0.0.0:8000

run_plus:
		@echo 'Corriendo server_plus...'
		@python manage.py $(LOCALSERVER_PLUS) 0.0.0.0:8000

syncdb:
		@echo 'Creando tablas y migraciones en la DB...'
		@python manage.py $(SYNCDB)

migrations:
		@echo 'Generando migraciones...'
		@python manage.py $(MAKEMIGRATION)

migrate:
		@echo 'Applying migrations...'
		@python manage.py $(MIGRATE)

syncdb_no_initial:
		@echo 'Creando tablas en la DB...'
		@python manage.py $(CREATEDB)

createsuperuser:
		@echo 'Crear superusuario'
		@python manage.py $(SUPERUSER)

shell:
		@echo 'Iniciando shell de Django...'
		@python manage.py $(CONSOLE)

shell_plus:
		@echo 'Iniciando shell_plus de Django...'
		@python manage.py $(CONSOLE_PLUS)

notebook:
		@echo 'Iniciando shell_plus de Django...'
		@python manage.py $(CONSOLE_PLUS) --notebook

dbshell:
		@echo 'Iniciando consola de db...'
		@python manage.py $(DBSHELL)

messages:
		@echo 'Preparando strings para traducir...'
		@python manage.py $(MESSAGES)

compilemessages:
		@echo 'Compilando mensajes...'
		@python manage.py $(COMPILEMESSAGES)

initdb:
		@../provisioning/init_db.sh

