# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-23 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20180223_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='cart',
        ),
        migrations.AddField(
            model_name='transaction',
            name='cart_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
