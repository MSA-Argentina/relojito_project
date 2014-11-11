# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20141030_1716'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['due_date'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
    ]
