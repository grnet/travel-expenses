# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0010_auto_20170517_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelinfo',
            name='distance',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
