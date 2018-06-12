# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0020_auto_20171117_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='total_cost_manual',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
