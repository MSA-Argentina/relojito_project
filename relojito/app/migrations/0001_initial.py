# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('contact_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('phone', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('color', models.CharField(max_length=10, null=True, blank=True)),
                ('external_url', models.URLField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('client', models.ForeignKey(to='app.Client')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectCollaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='app.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Project collaborator',
                'verbose_name_plural': 'Project collaborators',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResolutionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('is_finished', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Type of resolution',
                'verbose_name_plural': 'Types of resolutions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=200, null=True, blank=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('external_url', models.URLField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(to='app.Project')),
                ('resolved_as', models.ForeignKey(blank=True, to='app.ResolutionType', null=True)),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Type of task',
                'verbose_name_plural': 'Types of tasks',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='task_type',
            field=models.ForeignKey(to='app.TaskType'),
            preserve_default=True,
        ),
    ]
