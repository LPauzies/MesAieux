# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-16 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20161212_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='individu',
            options={'permissions': (('admin_famille', 'Peut administrer une famille'), ('confirmation', "Peut confirmer l'acces a une famille"), ('historien', 'Peut valider ou non un document'))},
        ),
    ]