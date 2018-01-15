# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0025_auto_20180111_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='additional_expenses',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='petition',
            name='additional_expenses_initial',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='petition',
            name='participation_cost',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='petition',
            name='participation_local_cost',
            field=models.DecimalField(default=0.0, blank=True, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='petition',
            name='total_cost_manual',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='accommodation_cost',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='accommodation_local_cost',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='transportation_cost',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
