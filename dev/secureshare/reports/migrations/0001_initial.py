# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 19:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='title')),
                ('file', models.FileField(default=None, upload_to='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('is_root', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='None', max_length=50)),
                ('short_description', models.TextField(default='', max_length=200)),
                ('detailed_description', models.TextField(default='', max_length=5000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_private', models.BooleanField(default=False)),
                ('encrypted', models.BooleanField(default=False)),
                ('file', models.FileField(default='0b0', upload_to='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RootFolder',
            fields=[
                ('folder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Folder')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='root_folder', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('reports.folder',),
        ),
        migrations.CreateModel(
            name='SubFolder',
            fields=[
                ('folder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Folder')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent_folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_folder', to='reports.Folder')),
            ],
            bases=('reports.folder',),
        ),
        migrations.AddField(
            model_name='report',
            name='parent_folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='reports.Folder'),
        ),
        migrations.AddField(
            model_name='fileupload',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.Report'),
        ),
    ]
