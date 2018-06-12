# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import texpenses.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0026_auto_20180115_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='texpenses.Country', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='petition',
            name='project',
            field=models.ForeignKey(to='texpenses.Project', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='petition',
            name='tax_office',
            field=models.ForeignKey(to='texpenses.TaxOffice', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='petition',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, validators=[texpenses.models.models.is_manager], to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='arrival_point',
            field=models.ForeignKey(related_name='travel_arrival_point', on_delete=django.db.models.deletion.PROTECT, blank=True, to='texpenses.City', null=True),
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='departure_point',
            field=models.ForeignKey(related_name='travel_departure_point', on_delete=django.db.models.deletion.PROTECT, blank=True, to='texpenses.City', null=True),
        ),
        migrations.AlterField(
            model_name='travelinfo',
            name='travel_petition',
            field=models.ForeignKey(related_name='travel_info', on_delete=django.db.models.deletion.PROTECT, to='texpenses.Petition'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tax_office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='texpenses.TaxOffice', null=True),
        ),
    ]
