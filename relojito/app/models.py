from __future__ import unicode_literals

import datetime
import re
from collections import Counter

from django.contrib.auth.models import User
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models import Count, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


def sort_by_value(x):
    t = x.values()
    return sorted(t, reverse=True)


# monkey-patching the User class
def get_tasks(self):
    """
    Returns a queryset with all the tasks belonging to the user
    """
    tasks = Task.objects.filter(owner=self)

    return tasks


def get_projects(self):
    projects = Project.objects.filter(
        task__owner=self).distinct()

    return projects


def get_owned_projects(self):
    owned_projects = Project.objects.filter(owner=self,
                                            is_active=True)

    return owned_projects


def get_collab_projects(self):
    collab_projects = Project.objects.filter(projectcollaborator__user=self,
                                             is_active=True)

    return collab_projects


def total_tasks_per_type(self):
    taskset = self.get_tasks()
    t = taskset.values('task_type__name').\
        annotate(Count('task_type')).order_by()

    px = [sort_by_value(x) for x in list(t)]
    return px


def total_hours_per_type(self):
    taskset = self.get_tasks()
    t = taskset.values('task_type__name').\
        annotate(Sum('total_hours')).order_by()
    return list(t)


def total_tasks_per_project(self):
    taskset = self.get_tasks()
    t = taskset.values('project__name').\
        annotate(Count('project'))
    px = [sort_by_value(x) for x in list(t)]
    return px


def total_hours_per_project(self):
    taskset = self.get_tasks()
    t = taskset.values('project__color', 'project__name', 'project__id').\
        annotate(Sum('total_hours')).order_by()

    return list(t)

def word_frequencies(self):
    taskset = self.get_tasks()
    nonwords = set(['/', 'de', 'y', 'en', 'para',
        'con', 'a', 'e', 'el', 'y', 'la', 'las', 'por', 'del'])
    words = []
    for t in taskset:
        for w in re.split(r'[\s,.:]+', t.name.lower()):
            if w not in nonwords:
                words.append(w)
    counts = Counter(words).most_common(100)
    total = len(words)
    frequencies = map(lambda (word, count):
            {'text': word, 'size': count, 'frequency': count/float(total)}, counts)
    return {'total': total, 'frequencies': frequencies}

User.add_to_class("get_tasks", get_tasks)
User.add_to_class("get_projects", get_projects)
User.add_to_class("get_owned_projects", get_owned_projects)
User.add_to_class("get_collab_projects", get_collab_projects)
User.add_to_class("total_tasks_per_type", total_tasks_per_type)
User.add_to_class("total_tasks_per_project", total_tasks_per_project)
User.add_to_class("total_hours_per_type", total_hours_per_type)
User.add_to_class("total_hours_per_project", total_hours_per_project)
User.add_to_class("word_frequencies", word_frequencies)


@python_2_unicode_compatible
class Holiday(models.Model):
    name = models.CharField(_('name'), max_length=200)
    date = models.DateField(_('date'))
    description = models.TextField(_('description'), null=True, blank=True)

    class Meta:
        verbose_name = _('Holiday')
        verbose_name_plural = _('Holidays')

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class Client(models.Model):
    name = models.CharField(_('name'), max_length=200)
    contact_name = models.CharField(
        _('contact_name'), max_length=200, null=True, blank=True)
    email = models.EmailField(_('email'), null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), null=True, blank=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))
    color = models.CharField(_('color'), max_length=10, null=True, blank=True)
    external_url = models.URLField(_('external_url'), null=True, blank=True)

    is_active = models.BooleanField(_('is_active'), default=True)
    owner = models.ForeignKey(User, null=True, verbose_name=_('owner'))
    due_date = models.DateField(_('due_date'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['due_date']

    def __str__(self):
        return "{}".format(self.name)

    @property
    def get_absolute_url(self):
        return "/project/%i/" % self.pk

    @property
    def total_hours(self):
        hours = Task.objects.filter(project=self).aggregate(Sum('total_hours'))
        return hours['total_hours__sum']

    @property
    def total_tasks(self):
        total = Task.objects.filter(project=self).count()
        return total


@python_2_unicode_compatible
class ProjectCollaborator(models.Model):

    """
    Defines which users can add tasks to the project
    """
    project = models.ForeignKey(Project, verbose_name=_('project'))
    user = models.ForeignKey(User, verbose_name=_('user'))

    class Meta:
        verbose_name = _('Project collaborator')
        verbose_name_plural = _('Project collaborators')

    def __str__(self):
        return "{} - {}".format(self.project.name, self.user.username)


@python_2_unicode_compatible
class TaskType(models.Model):
    name = models.CharField(_('task_type'), max_length=200)

    class Meta:
        verbose_name = _('Type of task')
        verbose_name_plural = _('Types of tasks')

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class Task(models.Model):
    name = models.CharField(_('name'), max_length=200)
    project = models.ForeignKey(Project, verbose_name=_('project'))
    task_type = models.ForeignKey(TaskType, verbose_name=_('task_type'))
    description = models.TextField(_('description'), max_length=200,
                                   null=True, blank=True)
    date = models.DateField(_('date'), default=datetime.date.today)
    total_hours = models.FloatField(_('total_hours'), validators=[
        MinValueValidator(0.5),
        MaxValueValidator(24),
        RegexValidator(r'^([0-9]{1,2}(\.[05])?)$',
                       'Only .5 numbers'),
    ])
    external_url = models.URLField(_('external_url'), null=True, blank=True)

    owner = models.ForeignKey(User, null=True, verbose_name=_('owner'))
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        get_latest_by = "created_at"

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return "/task/%i/" % self.pk

    @property
    def task_title(self):
        return self.name + ' (' + str(self.total_hours) + ' hs)'

    def to_dict(self):
        d = {
            "id": self.pk,
            "title": self.task_title,
            "start": self.date,
            "url": self.get_absolute_url(),
            "allDay": True,
            "color": self.project.color,
            "textColor": "black"
        }

        return d


@receiver(post_save, sender=ProjectCollaborator)
def notify_new_collaborator(sender, instance, **kwargs):
    from .tasks import mail_alert_new_collaborator

    mail_alert_new_collaborator.delay(instance)
