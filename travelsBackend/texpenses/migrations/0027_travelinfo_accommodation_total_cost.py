# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0026_auto_20180115_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelinfo',
            name='accommodation_total_cost',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
