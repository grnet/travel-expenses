# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Group

def create_helpdesk_and_permissions(apps, schema_editor):
    # Copy secretary's group permissions
    # Let's hope there's one.
    secretary = Group.objects.get(name='SECRETARY')
    permissions = secretary.permissions.all()
    helpdesk, _ = Group.objects.get_or_create(name='HELPDESK')
    helpdesk.permissions.add(*permissions)

class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0035_auto_20180427_0957'),
    ]

    operations = [
        migrations.RunPython(create_helpdesk_and_permissions)
    ]
