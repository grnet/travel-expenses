# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_accommodation_total_local_cost(apps, schema_editor):
    TravelInfo = apps.get_model('texpenses', 'TravelInfo')
    for travel_info in TravelInfo.objects.all():
        if travel_info.accommodation_local_cost:
            travel_info.accommodation_total_local_cost = \
                travel_info.accommodation_local_cost * travel_info.overnights_num_manual
            travel_info.save()


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0030_travelinfo_accommodation_total_local_cost'),
    ]

    operations = [
        migrations.RunPython(migrate_accommodation_total_local_cost),
    ]
