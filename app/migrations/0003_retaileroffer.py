# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150710_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetailerOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=250)),
                ('image_url', models.URLField(max_length=500, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('price', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('url', models.URLField(max_length=500, null=True, blank=True)),
                ('retailer', models.ForeignKey(to='app.Retailer')),
            ],
            options={
                'db_table': 'retailer_offers',
            },
            bases=(models.Model,),
        ),
    ]
