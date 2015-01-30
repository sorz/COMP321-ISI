# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-create_date']},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-purchase_date']},
        ),
    ]
