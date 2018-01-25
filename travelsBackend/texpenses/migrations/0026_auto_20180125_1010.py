# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texpenses', '0025_merge'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SecretaryCompensation',
        ),
        migrations.DeleteModel(
            name='SecretaryPetition',
        ),
        migrations.DeleteModel(
            name='SecretaryPetitionSubmission',
        ),
        migrations.DeleteModel(
            name='UserCompensation',
        ),
        migrations.DeleteModel(
            name='UserPetition',
        ),
        migrations.DeleteModel(
            name='UserPetitionSubmission',
        ),
    ]
