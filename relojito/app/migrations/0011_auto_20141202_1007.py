# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_holiday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='resolved_as',
        ),
        migrations.DeleteModel(
            name='ResolutionType',
        ),
    ]
