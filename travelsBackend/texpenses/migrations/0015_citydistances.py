# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0014_auto_20170524_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityDistances',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('distance', models.PositiveSmallIntegerField(blank=True)),
                ('from_city', models.ForeignKey(related_name='from_city', to='texpenses.City')),
                ('to_city', models.ForeignKey(related_name='to_city', to='texpenses.City')),
            ],
        ),
    ]
