# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesite', '0005_auto_20170217_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_file',
            field=models.CharField(null=True, max_length=255, blank=True),
        ),
    ]
