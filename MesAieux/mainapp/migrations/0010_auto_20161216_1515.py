# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-16 14:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20161216_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banque',
            options={},
        ),
        migrations.AddField(
            model_name='banque',
            name='validation',
            field=models.BooleanField(default=False),
        ),
    ]
