# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-10 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0004_auto_20170910_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='negative_review',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='entity',
            name='positive_review',
            field=models.IntegerField(default=0),
        ),
    ]
