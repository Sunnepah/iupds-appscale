# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-05 15:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iupdsmanager', '0003_auto_20160305_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
    ]
