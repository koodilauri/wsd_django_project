# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-05 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesite', '0005_auto_20170305_0946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='sid',
        ),
        migrations.AddField(
            model_name='payment',
            name='price',
            field=models.IntegerField(default=15),
            preserve_default=False,
        ),
    ]
