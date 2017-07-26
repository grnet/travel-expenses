# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0017_petition_timesheeted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('texpenses.petition',),
        ),
    ]
