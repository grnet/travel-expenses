# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0034_auto_20180319_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citydistances',
            name='distance',
            field=models.FloatField(),
        ),
    ]
