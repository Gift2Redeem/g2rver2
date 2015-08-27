# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=50, null=True, blank=True)),
                ('expiration_date', models.DateField(null=True, blank=True)),
                ('barcode', models.CharField(max_length=500, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'card',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardBalance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('balance', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('card', models.ForeignKey(to='app.Card')),
            ],
            options={
                'db_table': 'card_balance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('image_url', models.CharField(max_length=500, null=True, blank=True)),
                ('details', models.CharField(max_length=500, null=True, blank=True)),
                ('terms_and_conditions', models.CharField(max_length=500, null=True, blank=True)),
                ('redemption_information', models.CharField(max_length=500, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=500, null=True, blank=True)),
                ('min_amount', models.DecimalField(default=0.0, null=True, max_digits=8, decimal_places=2, blank=True)),
                ('max_amount', models.DecimalField(default=0.0, null=True, max_digits=8, decimal_places=2, blank=True)),
                ('has_expiration_date', models.BooleanField(default=True)),
                ('has_realtime_balance', models.BooleanField(default=True)),
                ('is_usable_online', models.BooleanField(default=True)),
                ('is_usable_in_store', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('has_pin', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'card_profile',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OneTimePassword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('otp', models.CharField(max_length=50)),
                ('otp_types', models.CharField(default=b'NEW', max_length=10, choices=[(b'NEW', b'New'), (b'FORGOT', b'Forgot'), (b'CARD', b'Card'), (b'OTHER', b'Other')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'one_time_password',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=150, null=True, blank=True)),
                ('description', models.TextField()),
                ('logo', models.URLField(max_length=500)),
                ('site_url', models.URLField(max_length=500, blank=True)),
                ('slick_deals_url', models.URLField(null=True, blank=True)),
            ],
            options={
                'db_table': 'retailer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RetailerLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('lat', models.DecimalField(max_digits=10, decimal_places=6)),
                ('lng', models.DecimalField(max_digits=10, decimal_places=6)),
                ('address', models.CharField(max_length=250)),
                ('address2', models.CharField(max_length=250, null=True, blank=True)),
                ('city', models.CharField(max_length=250)),
                ('state', models.CharField(max_length=250)),
                ('postal_code', models.CharField(max_length=250)),
                ('retailer', models.ForeignKey(to='app.Retailer')),
            ],
            options={
                'db_table': 'retailer_locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('google_id', models.CharField(max_length=200, null=True, verbose_name=b'google_id')),
                ('google_image', models.CharField(max_length=500, null=True, verbose_name=b'google_image')),
                ('facebook_id', models.CharField(max_length=200, null=True, verbose_name=b'facebook_id')),
                ('dob', models.DateField(null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='WalletCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('card', models.ForeignKey(to='app.Card')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'wallet_card',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='onetimepassword',
            name='user',
            field=models.ForeignKey(to='app.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardprofile',
            name='retailer',
            field=models.ForeignKey(to='app.Retailer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='card_profile',
            field=models.ForeignKey(to='app.CardProfile'),
            preserve_default=True,
        ),
    ]
