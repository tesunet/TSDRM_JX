# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-11-12 14:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faconstor', '0056_processrun_rto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processrun',
            name='rto',
        ),
    ]
