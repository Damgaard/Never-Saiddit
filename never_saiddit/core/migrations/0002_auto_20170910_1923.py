# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-10 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='state',
            field=models.PositiveSmallIntegerField(choices=[(10, 'Asked user to authorize'), (20, 'Received code and state'), (30, 'Authenticated as user on Reddit'), (40, 'Deleting comments'), (41, 'Deleting submissions'), (50, 'Finished'), (100, 'Unknown error'), (101, 'Access denied')], default=10, help_text='How far are we along in the process.'),
        ),
    ]
