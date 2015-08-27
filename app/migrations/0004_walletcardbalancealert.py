# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_retaileroffer'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletCardBalanceAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('message', models.CharField(max_length=250, null=True, blank=True)),
                ('trigger_balance', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('wallet_card', models.ForeignKey(to='app.WalletCard')),
            ],
            options={
                'db_table': 'wallet_card_balance_alert',
            },
            bases=(models.Model,),
        ),
    ]
