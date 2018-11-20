# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0038_auto_20180905_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='additional_expenses_grnet',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
