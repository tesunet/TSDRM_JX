# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2020-03-24 14:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faconstor', '0060_origin_log_restore'),
    ]

    operations = [
        migrations.AddField(
            model_name='processrun',
            name='log_restore',
            field=models.IntegerField(default=2, null=True, verbose_name='是否回滚日志'),
        ),
    ]
