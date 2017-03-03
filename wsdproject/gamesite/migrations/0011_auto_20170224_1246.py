# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-24 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesite', '0010_auto_20170224_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_url',
            field=models.URLField(blank=True, default=b'http://webcourse.cs.hut.fi/example_game.html', null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(default=b'testipeli', max_length=255, unique=True),
        ),
    ]