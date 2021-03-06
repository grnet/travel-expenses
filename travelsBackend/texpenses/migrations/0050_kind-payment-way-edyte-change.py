# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-09-11 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0049_mail_rate_limiting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='kind',
            field=models.CharField(choices=[['PRE', '\u03a0\u03c1\u03cc\u03b5\u03b4\u03c1\u03bf\u03c2 \u0394\u03a3'], ['MEM', '\u039c\u03ad\u03bb\u03bf\u03c2 \u0394\u03a3'], ['PER', '\u03a0\u03c1\u03bf\u03c3\u03c9\u03c0\u03b9\u03ba\u03cc'], ['EXE', '\u03a3\u03c4\u03ad\u03bb\u03b5\u03c7\u03bf\u03c2 \u0395\u0394\u03a5\u03a4\u0395'], ['COL', '\u03a3\u03c5\u03bd\u03b5\u03c1\u03b3\u03ac\u03c4\u03b7\u03c2']], max_length=100),
        ),
        migrations.AlterField(
            model_name='petition',
            name='participation_payment_way',
            field=models.CharField(choices=[['NON', '\u038c\u03c7\u03b9 \u03b1\u03ba\u03cc\u03bc\u03b7'], ['AGNT', '\u03a0\u03c1\u03b1\u03ba\u03c4\u03bf\u03c1\u03b5\u03af\u03bf'], ['GRNET', 'VISA \u0395\u0394\u03a5\u03a4\u0395'], ['VISA', '\u03a0\u03b9\u03c3\u03c4\u03c9\u03c4\u03b9\u03ba\u03ae \u039c\u03b5\u03c4/\u03bd\u03bf\u03c5'], ['BANK', 'Bank Transfer']], default=b'NON', max_length=10),
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='accommodation_payment_way',
            field=models.CharField(choices=[['NON', '\u038c\u03c7\u03b9 \u03b1\u03ba\u03cc\u03bc\u03b7'], ['AGNT', '\u03a0\u03c1\u03b1\u03ba\u03c4\u03bf\u03c1\u03b5\u03af\u03bf'], ['GRNET', 'VISA \u0395\u0394\u03a5\u03a4\u0395'], ['VISA', '\u03a0\u03b9\u03c3\u03c4\u03c9\u03c4\u03b9\u03ba\u03ae \u039c\u03b5\u03c4/\u03bd\u03bf\u03c5'], ['BANK', 'Bank Transfer']], default=b'NON', max_length=5),
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='transportation_payment_way',
            field=models.CharField(choices=[['NON', '\u038c\u03c7\u03b9 \u03b1\u03ba\u03cc\u03bc\u03b7'], ['AGNT', '\u03a0\u03c1\u03b1\u03ba\u03c4\u03bf\u03c1\u03b5\u03af\u03bf'], ['GRNET', 'VISA \u0395\u0394\u03a5\u03a4\u0395'], ['VISA', '\u03a0\u03b9\u03c3\u03c4\u03c9\u03c4\u03b9\u03ba\u03ae \u039c\u03b5\u03c4/\u03bd\u03bf\u03c5'], ['BANK', 'Bank Transfer']], default=b'NON', max_length=5),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='kind',
            field=models.CharField(choices=[['PRE', '\u03a0\u03c1\u03cc\u03b5\u03b4\u03c1\u03bf\u03c2 \u0394\u03a3'], ['MEM', '\u039c\u03ad\u03bb\u03bf\u03c2 \u0394\u03a3'], ['PER', '\u03a0\u03c1\u03bf\u03c3\u03c9\u03c0\u03b9\u03ba\u03cc'], ['EXE', '\u03a3\u03c4\u03ad\u03bb\u03b5\u03c7\u03bf\u03c2 \u0395\u0394\u03a5\u03a4\u0395'], ['COL', '\u03a3\u03c5\u03bd\u03b5\u03c1\u03b3\u03ac\u03c4\u03b7\u03c2']], max_length=100, null=True),
        ),
    ]
