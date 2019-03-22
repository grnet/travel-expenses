# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import pytz
from datetime import datetime
from django.db import migrations

logger = logging.getLogger(__name__)


def convert_datetimes(apps, schema_editor):
    Petition = apps.get_model('texpenses', 'Petition')
    bug_start_date = datetime(2018, 10, 4, tzinfo=pytz.UTC)
    for application in Petition.objects.filter(created__gt=bug_start_date):
        if not application.travel_info.exists():
            logger.info('Application w/ DSE %s has no travel infos, skipping' %
                        application.dse)
            continue
        fix_task_dates(application)
        for travel in application.travel_info.all():
            fix_depart_date(travel)
            fix_return_date(travel)
            travel.save()
        application.save()


def shift_time(dt, correct_tz):
    base_tz = pytz.timezone('Europe/Athens')
    base_offset = dt.astimezone(base_tz).utcoffset()
    correct_offset = dt.astimezone(correct_tz).utcoffset()
    shift_needed = base_offset - correct_offset
    dt += shift_needed
    return shift_needed


def fix_task_dates(application):
    local_city = application.travel_info.first().arrival_point
    correct_tz = pytz.timezone(local_city.timezone)
    start_shifted = shift_time(application.task_start_date, correct_tz)
    end_shifted = shift_time(application.task_end_date, correct_tz)
    logger.info('Application %s, task_start_date shifted %s' %
                (application.id, start_shifted))
    logger.info('Application %s, task_end_date shifted %s' %
                (application.id, end_shifted))


def fix_depart_date(travel):
    if not travel.depart_date:
        return
    correct_tz = pytz.timezone(travel.departure_point.timezone)
    shifted = shift_time(travel.depart_date, correct_tz)
    logger.info('Travel %s, depart_date shifted %s' %
                (travel.id, shifted))


def fix_return_date(travel):
    if not travel.return_date:
        return
    correct_tz = pytz.timezone(travel.arrival_point.timezone)
    shifted = shift_time(travel.return_date, correct_tz)
    logger.info('Travel %s, return_date shifted %s' %
                (travel.id, shifted))


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0040_merge'),
    ]

    operations = [
        migrations.RunPython(convert_datetimes),
    ]
