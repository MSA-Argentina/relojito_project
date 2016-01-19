# -*- coding: utf-8 -*-
from datetime import date, timedelta
from subprocess import check_output

from celery import task
from django.template.loader import render_to_string
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from .models import Holiday, Task


def get_fortune():
    """
    Get a random fortune from the system
    """
    fortune = check_output(['fortune'])

    return fortune


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


@task
def send_alert_to_user(user):
    subject = "No creaste tareas en Relojito ayer"
    project_url = settings.SITE_URL
    last_task = user.get_last_task()
    fortune = get_fortune()

    data = {
        "username": user.username,
        "project_url": project_url,
        "last_task": last_task,
        "fortune": fortune
    }

    text_body = render_to_string(
        'mails/no_tasks_yesterday.txt', data)

    to_mail = []
    to_mail.append(user.email)
    print(text_body)
    send_mail(
        subject, text_body, settings.DEFAULT_FROM_EMAIL, to_mail)


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
                send_alert_to_user.delay(user)


@task()
def mail_new_year_greeting():
    """
    Sends a happy new year greeting
    """
    users = User.objects.filter(is_active=True).all()

    for user in users:
        if user.email and user.username not in settings.ALERT_USERS_BLACKLIST:
            if not verify_yesterday_tasks(user):
                taskset = user.get_tasks()
                projects = user.get_projects()

                tx = taskset.aggregate(Sum('total_hours'))
                total_hours = tx['total_hours__sum']

                subject = _(u"Feliz año nuevo de parte de Relojito")
                body = _(u"""Hola %(username)s, Relojito te cuenta que hasta ahora completaste %(total_tareas)s tareas,
para un total de %(total_proyectos)s proyectos. En total, cargaste %(total_horas)s horas.\n
Más allá de las estadísticas, Relojito te desea un excelente comienzo de año!""") % {'total_tareas': len(taskset),
                                                                                     'username': user.first_name,
                                                                                     'total_proyectos': len(projects),
                                                                                     'total_horas': total_hours
                                                                                     }
                to_mail = []
                to_mail.append(user.email)
                print(user.username, subject, body)
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, to_mail)


@task()
def mail_alert_new_collaborator(instance):
    project_name = instance.project.name
    project_url = settings.SITE_URL + instance.project.get_absolute_url
    subject = _(u'You are now a collaborator in %(project_name)s') % {
        'project_name': project_name}
    body = _(u"""Hi, you've been added as a colaborator in %(project_name)s.\n\n
    Check the details at %(project_url)s.\n\n  Bye!""") % {'project_name': project_name,
                                                           'project_url': project_url}
    to_mail = []
    to_mail.append(instance.user.email)
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, to_mail)
