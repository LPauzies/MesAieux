# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-23 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20161221_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individu',
            name='date_dece',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]