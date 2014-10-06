from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        return "{}".format(self.name)


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client)
    color = models.CharField(max_length=10, null=True, blank=True)
    external_url = models.URLField(null=True, blank=True)

    owner = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return "{}".format(self.name)


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


class TaskType(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('Type of task')
        verbose_name_plural = _('Types of tasks')

    def __str__(self):
        return "{}".format(self.name)


class ResolutionType(models.Model):
    name = models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Type of resolution')
        verbose_name_plural = _('Types of resolutions')

    def __str__(self):
        return "{}".format(self.name)


class Task(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    task_type = models.ForeignKey(TaskType)
    description = models.TextField(max_length=200, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    resolved_as = models.ForeignKey(ResolutionType, null=True, blank=True)
    external_url = models.URLField(null=True, blank=True)

    owner = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return "/task/%i/" % self.pk

    @property
    def total_hours(self):
        diff = self.end - self.start

        return float(diff.seconds / 3600.0)

    def to_dict(self):
        d = {
            "id": self.pk,
            "title": self.name,
            "start": self.start,
            "end": self.end,
            "url": self.get_absolute_url(),
            "allDay": False,
            "color": self.project.color,
            "textColor": "black"
        }

        return d
