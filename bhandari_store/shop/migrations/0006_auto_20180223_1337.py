# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-23 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_transaction_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
