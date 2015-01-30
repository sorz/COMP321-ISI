# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20150120_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='writer',
        ),
        migrations.AddField(
            model_name='message',
            name='by_vendor',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
