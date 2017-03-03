# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesite', '0006_game_game_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_file',
            field=models.URLField(default=None, null=True, blank=True),
        ),
    ]
