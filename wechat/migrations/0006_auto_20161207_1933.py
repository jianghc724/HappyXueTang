# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-07 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0005_auto_20161207_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourse',
            name='status',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]