# coding: utf-8
from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'relojito.settings.development')

app = Celery('relojito')
app.config_from_object('django.conf:settings')

# Autodiscover tasks on each app
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    """
    Task to debug Celery
    """
    print('Request: {0!r}'.format(self.request))
