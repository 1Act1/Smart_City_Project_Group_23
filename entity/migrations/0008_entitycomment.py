# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-09 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0007_auto_20171009_0607'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntityComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_id', models.IntegerField()),
                ('comment', models.CharField(max_length=300)),
            ],
        ),
    ]
