# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-07 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_auto_20161207_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(db_index=True, max_length=16),
        ),
    ]
