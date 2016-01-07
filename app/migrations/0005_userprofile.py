# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_walletcardbalancealert'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile', models.CharField(max_length=200, null=True, verbose_name=b'mobile')),
                ('user_image', models.ImageField(null=True, upload_to=b'images', blank=True)),
                ('google_id', models.CharField(max_length=200, null=True, verbose_name=b'google_id')),
                ('google_image', models.CharField(max_length=500, null=True, verbose_name=b'google_image')),
                ('facebook_id', models.CharField(max_length=200, null=True, verbose_name=b'facebook_id')),
                ('dob', models.DateField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
