# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0017_petition_timesheeted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='travelinfo',
            options={'ordering': ['depart_date']},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='kind',
            field=models.CharField(max_length=100, null=True, choices=[['PRE', '\u03a0\u03c1\u03cc\u03b5\u03b4\u03c1\u03bf\u03c2 \u0394\u03a3'], ['MEM', '\u039c\u03ad\u03bb\u03bf\u03c2 \u0394\u03a3'], ['PER', '\u03a0\u03c1\u03bf\u03c3\u03c9\u03c0\u03b9\u03ba\u03cc'], ['EXE', '\u03a3\u03c4\u03ad\u03bb\u03b5\u03c7\u03bf\u03c2 \u0395\u0394\u0395\u03a4'], ['COL', '\u03a3\u03c5\u03bd\u03b5\u03c1\u03b3\u03ac\u03c4\u03b7\u03c2']]),
        ),
    ]
