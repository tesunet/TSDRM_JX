# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-09-09 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faconstor', '0028_clientmanage'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmanage',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='状态'),
        ),
    ]