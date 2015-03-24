# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20150205_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sale_amount',
            field=models.DecimalField(max_digits=12, default=0, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='sale_quantity',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
