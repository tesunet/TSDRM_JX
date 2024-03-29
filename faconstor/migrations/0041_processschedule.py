# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-09-29 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '0001_initial'),
        ('faconstor', '0040_target_data_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='计划说明')),
                ('dj_periodictask', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='djcelery.PeriodicTask', verbose_name='定时任务')),
                ('process', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='faconstor.Process', verbose_name='流程预案')),
            ],
        ),
    ]
