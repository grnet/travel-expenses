# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0007_auto_20170420_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='timezone',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
