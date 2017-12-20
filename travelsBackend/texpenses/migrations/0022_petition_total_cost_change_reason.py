# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0021_petition_total_cost_manual'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='total_cost_change_reason',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
