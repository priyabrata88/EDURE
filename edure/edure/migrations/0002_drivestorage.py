# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-18 17:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('edure', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriveStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('timestamp_mod', models.DateTimeField(blank=True, null=True)),
                ('files', models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to=b'upload')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
