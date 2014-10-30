# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20141016_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='contact_name',
            field=models.CharField(max_length=200, null=True, verbose_name='contact_name', blank=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=75, null=True, verbose_name='email', blank=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=200, null=True, verbose_name='phone', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.ForeignKey(verbose_name='client', to='app.Client'),
        ),
        migrations.AlterField(
            model_name='project',
            name='color',
            field=models.CharField(max_length=10, null=True, verbose_name='color', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='external_url',
            field=models.URLField(null=True, verbose_name='external_url', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is_active'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(verbose_name='owner', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='projectcollaborator',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='app.Project'),
        ),
        migrations.AlterField(
            model_name='projectcollaborator',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='resolutiontype',
            name='is_finished',
            field=models.BooleanField(default=False, verbose_name='is_finished'),
        ),
        migrations.AlterField(
            model_name='resolutiontype',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=200, null=True, verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='external_url',
            field=models.URLField(null=True, verbose_name='external_url', blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(verbose_name='owner', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(verbose_name='project', to='app.Project'),
        ),
        migrations.AlterField(
            model_name='task',
            name='resolved_as',
            field=models.ForeignKey(verbose_name='resolved_as', blank=True, to='app.ResolutionType', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(verbose_name='task_type', to='app.TaskType'),
        ),
        migrations.AlterField(
            model_name='task',
            name='total_hours',
            field=models.FloatField(verbose_name='total_hours', validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.RegexValidator('^(\\d(\\.[05])?)$', 'Only .5 numbers')]),
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='name',
            field=models.CharField(max_length=200, verbose_name='task_type'),
        ),
    ]
