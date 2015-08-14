# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20150812_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 26, 50, 283361)),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 26, 50, 284239)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 26, 50, 274249)),
        ),
    ]