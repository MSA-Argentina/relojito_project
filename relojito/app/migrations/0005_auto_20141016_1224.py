# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_project_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'get_latest_by': 'created_at', 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
