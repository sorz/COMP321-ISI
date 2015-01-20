# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20150119_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='name',
        ),
        migrations.RemoveField(
            model_name='property',
            name='product',
        ),
        migrations.DeleteModel(
            name='Property',
        ),
    ]
