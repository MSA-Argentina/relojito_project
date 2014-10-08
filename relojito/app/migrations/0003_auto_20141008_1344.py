# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20141007_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='end',
        ),
        migrations.RemoveField(
            model_name='task',
            name='start',
        ),
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateField(default=datetime.date(2014, 10, 8)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='total_hours',
            field=models.FloatField(default=3, validators=[django.core.validators.MinValueValidator(0.5), django.core.validators.RegexValidator('^(\\d(\\.[05])?)$', 'Only .5 numbers')]),
            preserve_default=False,
        ),
    ]
