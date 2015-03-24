# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20150324_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.RemoveField(
            model_name='product',
            name='off_shelf',
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('N', 'In stock'), ('O', 'Out of stock'), ('F', 'Off shelf')], max_length=1, default='N'),
            preserve_default=True,
        ),
    ]
