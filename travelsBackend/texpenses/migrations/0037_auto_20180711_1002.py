# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0036_auto_20180622_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='compensation_decision_protocol',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='compensation_petition_protocol',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='expenditure_protocol',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='movement_protocol',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
