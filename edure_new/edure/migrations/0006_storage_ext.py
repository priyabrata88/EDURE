# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-24 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edure', '0005_storage_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='storage',
            name='ext',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
