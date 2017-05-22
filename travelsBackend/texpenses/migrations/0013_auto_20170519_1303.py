# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0012_auto_20170519_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travelinfo',
            name='means_of_transport',
            field=models.CharField(default=b'AIR', max_length=10, choices=[['B\u0399\u039a\u0395', '\u039c\u03b7\u03c7\u03b1\u03bd\u03ae'], ['TRAIN', '\u03a4\u03c1\u03b1\u03af\u03bd\u03bf'], ['SHIP', '\u039a\u03b1\u03c1\u03ac\u03b2\u03b9'], ['AIR', '\u0391\u03b5\u03c1\u03bf\u03c0\u03bb\u03ac\u03bd\u03bf'], ['CAR', '\u0391\u03c5\u03c4\u03bf\u03ba\u03af\u03bd\u03b7\u03c4\u03bf'], ['BUS', '\u039b\u03b5\u03c9\u03c6\u03bf\u03c1\u03b5\u03af\u03bf']]),
        ),
    ]
