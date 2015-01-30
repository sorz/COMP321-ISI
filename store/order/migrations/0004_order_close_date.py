# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20150127_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='close_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
