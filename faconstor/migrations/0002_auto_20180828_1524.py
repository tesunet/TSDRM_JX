# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-08-28 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faconstor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifyitems',
            name='step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faconstor.Step'),
        ),
    ]
