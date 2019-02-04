# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from datetime import datetime
from django.db import migrations, models

def convert_datetimes(apps, schema_editor):
    Applications = apps.get_model('texpenses', 'Applications')
    bug_start_date = datetime.now()
    for application in Applications.objects.filter(created__gt=bug_start_date):
        travel_infos = list(application.travel_info.all())
        if not travel_infos:
            continue
        fix_task_start_date(application)
        fix_task_end_date(application)
        for travel in travel_infos:
            fix_depart_date(travel)
            fix_return_date(travel)
            travel.save()
        application.save()

def fix_task_start_date(application):
    base_tz = pytz.timezone('Europe/Athens')
    travel_infos = list(application.travel_info.all())
    correct_tz = travel_infos[0].arrival_point.timezone
    shift_needed = (base_tz.utcoffset(application.created) -
        pytz.timezone(correct_tz).utcoffset(application.created))
    application.task_start_date += shift_needed

def fix_task_end_date(application):
    base_tz = pytz.timezone('Europe/Athens')
    travel_infos = list(application.travel_info.all())
    correct_tz = travel_infos[-1].arrival_point.timezone
    shift_needed = (base_tz.utcoffset(application.created) -
        pytz.timezone(correct_tz).utcoffset(application.created))
    application.task_end_date += shift_needed

def fix_depart_date(travel):
    base_tz = pytz.timezone('Europe/Athens')
    if not travel.depart_date:
        return
    correct_tz = travel.departure_point.timezone
    shift_needed = (base_tz.utcoffset(travel.created) -
        pytz.timezone(correct_tz).utcoffset(travel.created))
    travel.depart_date += shift_needed

def fix_return_date(travel):
    base_tz = pytz.timezone('Europe/Athens')
    if not travel.return_date:
        return
    correct_tz = travel.arrival_point.timezone
    shift_needed = (base_tz.utcoffset(travel.created) -
        pytz.timezone(correct_tz).utcoffset(travel.created))
    travel.arrival_date += shift_needed


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0040_merge'),
    ]

    operations = [
        migrations.RunPython(convert_datetimes),
    ]
