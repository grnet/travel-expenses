# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0006_auto_20170407_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='petition',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
