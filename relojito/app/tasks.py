# -*- coding: utf-8 -*-
from datetime import date, timedelta

from celery import task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from .models import Holiday, Task


def verify_yesterday_tasks(user):
    """
    Returns True if a user created at least one task
    yesterday. Checks if 'yesterday' was on weekend or was
    a holiday.
    """
    yesterday = date.today() - timedelta(days=1)

    if Holiday.objects.filter(date=yesterday).exists() or \
       yesterday.weekday() in [5, 6]:

        return True

    return Task.objects.filter(date=yesterday, owner=user).exists()


@task()
def mail_alert_no_created_task():
    """
    Sends an alert if a user didn't create any tasks the
    day before
    """
    users = User.objects.filter(is_active=True).all()

    for user in users:
        if user.email and user.username not in settings.ALERT_USERS_BLACKLIST:
            if not verify_yesterday_tasks(user):
                subject = _(u"You haven't created any tasks in Relojito yesterday")
                project_url = settings.SITE_URL
                body = _(u"""Hi %(username)s, this is a friendly reminder that you haven't created a task in Relojito yesterday.\n
                Please go to %(project_url)s.\n\n  Bye!""") % {'project_url': project_url, 'username': user.first_name}
                to_mail = []
                to_mail.append(user.email)
                print user.username, subject, body
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, to_mail)


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