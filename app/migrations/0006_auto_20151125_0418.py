# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='facebook_id',
            field=models.CharField(max_length=200, unique=True, null=True, verbose_name=b'facebook_id'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='google_id',
            field=models.CharField(max_length=200, unique=True, null=True, verbose_name=b'google_id'),
        ),
    ]
