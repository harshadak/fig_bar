# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-05 01:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0008_auto_20170905_0139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='users_quotes',
            new_name='fav_quotes',
        ),
    ]
