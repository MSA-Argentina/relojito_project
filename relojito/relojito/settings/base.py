# -*- coding: utf-8 -*-
import os

from celery.schedules import crontab


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DJANGO_SETTINGS_MODULE = 'relojito.settings.base'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'bootstrap3',
    'crispy_forms',
    'captcha',

    'app'
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'relojito.urls'

WSGI_APPLICATION = 'relojito.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'relojito',
        'USER': '',
        'PASSWORD': '',
        'HOST': ''
    }
}
TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True
USE_TZ = True
LANGUAGE_CODE = 'es_AR'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'

# crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

BOOTSTRAP3 = {
    # The Bootstrap base URL
    'base_url': 'http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/'
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGINATE_BY': None,
}

# Celery / Redis broker
BROKER_URL = 'redis://127.0.0.1:6379/0'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CELERY_ACCEPT_CONTENT = ['pickle', 'json']
# CELERY_USER = 'relojito'
# CELERY_GROUP = 'relojito'

CELERYBEAT_SCHEDULE = {
    # Executes every morning at 9:30 A.M
    'nag-users-every-day': {
        'task': 'app.tasks.mail_alert_no_created_task',
        'schedule': crontab(hour=9, minute=30)
    },
    # Executes every monday, 9:45 AM
    'weekly_summary': {
        'task': 'app.tasks.mail_weekly_summary',
        'schedule': crontab(hour=9, minute=45, day_of_week='mon')
    },
}

ALERT_USERS_BLACKLIST = []
