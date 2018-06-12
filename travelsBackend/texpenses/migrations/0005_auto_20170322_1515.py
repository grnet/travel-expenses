# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0004_auto_20161219_1641'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TravelInfoCompensation',
        ),
        migrations.DeleteModel(
            name='TravelInfoSecretarySubmission',
        ),
        migrations.DeleteModel(
            name='TravelInfoUserSubmission',
        ),
        migrations.AlterField(
            model_name='petition',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 15, 15, 59, 387575)),
        ),
        migrations.AlterField(
            model_name='petition',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 15, 15, 59, 387615)),
        ),
    ]
