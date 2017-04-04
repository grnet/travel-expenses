# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0003_auto_20161219_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 19, 16, 41, 22, 929524)),
        ),
        migrations.AlterField(
            model_name='petition',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 19, 16, 41, 22, 929579)),
        ),
    ]
