# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0016_project_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='timesheeted',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
