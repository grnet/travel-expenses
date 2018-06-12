# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import datetime, time
from pytz import timezone


def update_time(apps, schema_editor):
    Petition = apps.get_model('texpenses', 'Petition')

    utc = timezone('UTC')
    t = time(12, 0)
    for p in Petition.objects.all():
        if p.compensation_decision_date:
            cdd = datetime.combine(p.compensation_decision_date, t)
            cdd = utc.localize(cdd)
            p.compensation_decision_date = cdd
        if p.compensation_petition_date:
            cpd = datetime.combine(p.compensation_petition_date, t)
            cpd = utc.localize(cpd)
            p.compensation_petition_date = cpd
        if p.expenditure_date_protocol:
            edp = datetime.combine(p.expenditure_date_protocol, t)
            edp = utc.localize(edp)
            p.expenditure_date_protocol = edp
        if p.movement_date_protocol:
            mdp = datetime.combine(p.movement_date_protocol, t)
            mdp = utc.localize(mdp)
            p.movement_date_protocol = mdp
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0033_auto_20180319_1236'),
    ]

    operations = [
        migrations.RunPython(update_time)
    ]
