# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-19 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20161216_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banque',
            name='fichier',
            field=models.FileField(upload_to='/uploads/'),
        ),
    ]
