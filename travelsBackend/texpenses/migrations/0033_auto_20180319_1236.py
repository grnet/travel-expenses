# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0032_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='compensation_decision_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='compensation_petition_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='expenditure_date_protocol',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='movement_date_protocol',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
