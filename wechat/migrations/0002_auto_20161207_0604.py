# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-07 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_time',
            field=models.IntegerField(),
        ),
    ]
