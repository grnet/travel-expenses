# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
import texpenses.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0006_auto_20170407_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='petition',
            name='manager_final_approval',
        ),
        migrations.RemoveField(
            model_name='petition',
            name='manager_travel_approval',
        ),
        migrations.RemoveField(
            model_name='project',
            name='manager_email',
        ),
        migrations.RemoveField(
            model_name='project',
            name='manager_name',
        ),
        migrations.RemoveField(
            model_name='project',
            name='manager_surname',
        ),
        migrations.AddField(
            model_name='petition',
            name='manager_cost_approval',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='petition',
            name='manager_movement_approval',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AddField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(validators=[texpenses.models.models.is_manager], to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 7, 16, 38, 35, 958341)),
        ),
        migrations.AlterField(
            model_name='petition',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 7, 16, 38, 35, 958373)),
        ),
    ]
