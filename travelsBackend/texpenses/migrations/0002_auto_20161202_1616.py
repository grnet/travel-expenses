# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 2, 16, 16, 31, 269995)),
        ),
        migrations.AlterField(
            model_name='petition',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 2, 16, 16, 31, 270038)),
        ),
    ]
