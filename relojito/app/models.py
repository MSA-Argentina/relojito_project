from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Client(models.Model):
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client)
    color = models.CharField(max_length=10, null=True, blank=True)
    external_url = models.URLField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return "{}".format(self.name)

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
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _('Project collaborator')
        verbose_name_plural = _('Project collaborators')

    def __str__(self):
        return "{} - {}".format(self.project.name, self.user.username)


@python_2_unicode_compatible
class TaskType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Type of task')
        verbose_name_plural = _('Types of tasks')

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class ResolutionType(models.Model):
    name = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Type of resolution')
        verbose_name_plural = _('Types of resolutions')

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class Task(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    task_type = models.ForeignKey(TaskType)
    description = models.TextField(max_length=200, null=True, blank=True)
    date = models.DateField(default=datetime.date.today())
    total_hours = models.FloatField(validators=[
        MinValueValidator(0.5),
        RegexValidator(r'^(\d(\.[05])?)$',
                       'Only .5 numbers'),
    ])
    resolved_as = models.ForeignKey(ResolutionType, null=True, blank=True)
    external_url = models.URLField(null=True, blank=True)

    owner = models.ForeignKey(User, null=True)
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
