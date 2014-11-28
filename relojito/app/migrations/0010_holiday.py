# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20141111_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('date', models.DateField(verbose_name='date')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'Holiday',
                'verbose_name_plural': 'Holidays',
            },
            bases=(models.Model,),
        ),
    ]
