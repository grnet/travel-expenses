# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0038_auto_20180905_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelinfo',
            name='no_transportation_calculation',
            field=models.BooleanField(default=False),
        ),
    ]
