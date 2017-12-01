# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0020_auto_20171117_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='withdrawn',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
