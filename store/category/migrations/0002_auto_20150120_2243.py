# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20150120_2243'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyname',
            name='category',
        ),
        migrations.DeleteModel(
            name='PropertyName',
        ),
    ]
