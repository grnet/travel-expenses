# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-11-19 10:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0053_add-EUR-default-value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='non_grnet_quota',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
    ]
