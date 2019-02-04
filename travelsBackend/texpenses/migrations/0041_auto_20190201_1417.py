# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from datetime import datetime
from django.db import migrations, models

base_tz = pytz.timezone('Europe/Athens')

def convert_datetimes(apps, schema_editor):
    Applications = apps.get_model('texpenses', 'Applications')
    #TODO this datetime has to be investigated
    bug_start_date = datetime(2018,10,1,tzinfo=pytz.UTC)
    for application in Applications.objects.filter(updated__gt=bug_start_date):
        if not application.travel_info.exists():
            continue
        fix_task_start_date(application)
        fix_task_end_date(application)
        for travel in application.travel_info.all():
            fix_depart_date(travel)
            fix_return_date(travel)
            travel.save()
        application.save()

def fix_task_start_date(application):
    local_city = application.travel_info.first().arrival_point
    correct_tz = pytz.timezone(local_city.timezone)
    shift_needed = (application.updated.astimezone(base_tz).utcoffset() -
        application.updated.astimezone(correct_tz).utcoffset())
    application.task_start_date += shift_needed

def fix_task_end_date(application):
    local_city = application.travel_info.last().arrival_point
    correct_tz = pytz.timezone(local_city.timezone)
    shift_needed = (application.updated.astimezone(base_tz).utcoffset() -
        application.updated.astimezone(correct_tz).utcoffset())
    application.task_end_date += shift_needed

def fix_depart_date(travel):
    if not travel.depart_date:
        return
    correct_tz = pytz.timezone(travel.departure_point.timezone)
    time_updated = travel.travel_petition.updated
    shift_needed = (time_updated.astimezone(base_tz).utcoffset() -
        time_updated.astimezone(correct_tz).utcoffset())
    travel.depart_date += shift_needed

def fix_return_date(travel):
    if not travel.return_date:
        return
    correct_tz = pytz.timezone(travel.arrival_point.timezone)
    time_updated = travel.travel_petition.updated
    shift_needed = (time_updated.astimezone(base_tz).utcoffset() -
        time_updated.astimezone(correct_tz).utcoffset())
    travel.return_date += shift_needed


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0040_merge'),
    ]

    operations = [
        migrations.RunPython(convert_datetimes),
    ]
