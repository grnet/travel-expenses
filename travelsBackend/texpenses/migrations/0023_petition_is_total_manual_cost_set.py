# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0022_petition_total_cost_change_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='is_total_manual_cost_set',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
