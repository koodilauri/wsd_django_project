# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('gamesite', '0004_auto_20170126_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, default='', max_length=255)),
                ('developer', models.CharField(max_length=250)),
                ('genre', models.TextField(default='')),
                ('image_url', models.URLField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default=datetime.datetime(2017, 2, 17, 4, 57, 30, 778745, tzinfo=utc), max_length=120),
            preserve_default=False,
        ),
    ]
