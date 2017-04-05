# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import texpenses.models.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0008_auto_20170405_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 5, 14, 0, 3, 334465)),
        ),
        migrations.AlterField(
            model_name='petition',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 5, 14, 0, 3, 334495)),
        ),
        migrations.AlterField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(validators=[texpenses.models.models.is_manager], to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
    ]
