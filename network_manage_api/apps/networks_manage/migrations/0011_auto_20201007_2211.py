# Generated by Django 2.0.6 on 2020-10-07 14:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networks_manage', '0010_auto_20201007_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networks',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 7, 22, 11, 58, 435415), verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='networks',
            name='query_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 7, 22, 11, 58, 435384), verbose_name='最新探测时间'),
        ),
    ]
