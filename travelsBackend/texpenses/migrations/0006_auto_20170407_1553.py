# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import texpenses.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0005_auto_20170322_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 7, 15, 53, 12, 669718)),
        ),
        migrations.AlterField(
            model_name='petition',
            name='iban',
            field=models.CharField(max_length=27, validators=[texpenses.validators.iban_validation]),
        ),
        migrations.AlterField(
            model_name='petition',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 7, 15, 53, 12, 669747)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='iban',
            field=models.CharField(max_length=27, null=True, validators=[texpenses.validators.iban_validation]),
        ),
    ]
