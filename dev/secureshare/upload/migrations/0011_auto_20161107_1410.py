# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 19:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0010_auto_20161107_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 7, 14, 10, 38, 714773)),
        ),
    ]
