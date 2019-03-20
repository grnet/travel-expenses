# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
from datetime import datetime
from django.db import migrations


def convert_datetimes(apps, schema_editor):
    Petition = apps.get_model('texpenses', 'Petition')
    bug_start_date = datetime(2018, 10, 4, tzinfo=pytz.UTC)
    for application in Petition.objects.filter(created__gt=bug_start_date):
        if not application.travel_info.exists():
            continue
        fix_task_dates(application)
        for travel in application.travel_info.all():
            fix_depart_date(travel)
            fix_return_date(travel)
            travel.save()
        application.save()


def calculate_shift_needed(time_created, correct_tz):
    base_tz = pytz.timezone('Europe/Athens')
    base_offset = time_created.astimezone(base_tz).utcoffset()
    correct_offset = time_created.astimezone(correct_tz).utcoffset()
    return (base_offset - correct_offset)


def fix_task_dates(application):
    local_city = application.travel_info.first().arrival_point
    correct_tz = pytz.timezone(local_city.timezone)
    shift_needed = calculate_shift_needed(application.created, correct_tz)
    application.task_start_date += shift_needed
    application.task_end_date += shift_needed


def fix_depart_date(travel):
    if not travel.depart_date:
        return
    correct_tz = pytz.timezone(travel.departure_point.timezone)
    time_created = travel.travel_petition.created
    shift_needed = calculate_shift_needed(time_created, correct_tz)
    travel.depart_date += shift_needed


def fix_return_date(travel):
    if not travel.return_date:
        return
    correct_tz = pytz.timezone(travel.arrival_point.timezone)
    time_created = travel.travel_petition.created
    shift_needed = calculate_shift_needed(time_created, correct_tz)
    travel.return_date += shift_needed


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0040_merge'),
    ]

    operations = [
        migrations.RunPython(convert_datetimes),
    ]
