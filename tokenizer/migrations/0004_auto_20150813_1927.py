# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tokenizer', '0003_auto_20150813_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 19, 27, 0, 954436)),
        ),
    ]