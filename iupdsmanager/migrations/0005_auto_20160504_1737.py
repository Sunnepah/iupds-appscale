# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-04 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iupdsmanager', '0004_auto_20160504_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='client_id',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
