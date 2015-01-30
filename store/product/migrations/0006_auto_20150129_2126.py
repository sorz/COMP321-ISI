# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20150120_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=sorl.thumbnail.fields.ImageField(upload_to='photos/%Y/%m'),
            preserve_default=True,
        ),
    ]
