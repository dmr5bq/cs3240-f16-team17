# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 17:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_auto_20161107_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 7, 12, 22, 17, 470358)),
        ),
    ]
