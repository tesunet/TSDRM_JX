# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2020-03-24 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faconstor', '0059_processrun_recover_end_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='origin',
            name='log_restore',
            field=models.IntegerField(choices=[(1, '是'), (2, '否')], default=2, null=True, verbose_name='是否回滚日志'),
        ),
    ]
