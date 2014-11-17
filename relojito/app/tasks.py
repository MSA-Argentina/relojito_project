# -*- coding: utf-8 -*-

from celery import task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext as _


@task()
def mail_alert_new_collaborator(instance):
    project_name = instance.project.name
    project_url = settings.SITE_URL + instance.project.get_absolute_url
    subject = _(u'You are now a collaborator in %(project_name)s') % {'project_name': project_name}
    body = _(u"""Hi, you've been added as a colaborator in %(project_name)s.\n\n
    Check the details at %(project_url)s.\n\n  Bye!""") % {'project_name': project_name,
                                                           'project_url': project_url}
    to_mail = []
    to_mail.append(instance.user.email)
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, to_mail)
