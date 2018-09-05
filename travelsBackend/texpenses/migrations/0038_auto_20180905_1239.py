# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0037_auto_20180711_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='initial_user_days_left',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='petition',
            name='transport_days_total',
            field=models.IntegerField(default=0),
        ),
    ]
