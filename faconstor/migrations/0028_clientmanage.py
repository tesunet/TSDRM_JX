# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-09-09 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faconstor', '0027_hostsmanage_host_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.IntegerField(blank=True, null=True, verbose_name='客户端ID')),
                ('client_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='客户端名称')),
                ('client_os', models.CharField(blank=True, max_length=64, null=True, verbose_name='操作系统')),
                ('install_time', models.DateTimeField(blank=True, null=True, verbose_name='安装时间')),
            ],
        ),
    ]