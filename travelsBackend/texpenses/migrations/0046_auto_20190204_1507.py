# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-02-04 15:07
from __future__ import unicode_literals

from django.db import migrations


def migrate_files_to_petitions(apps, schema_editor):
    Petition = apps.get_model('texpenses', 'Petition')
    TravelFile = apps.get_model('texpenses', 'TravelFile')

    for tf in TravelFile.objects.all():
        p = Petition.objects.get(id=tf.source_id)
        p.travel_files.add(tf)

class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0045_auto_20190204_1506'),
    ]

    operations = [
        migrations.RunPython(migrate_files_to_petitions)
    ]
