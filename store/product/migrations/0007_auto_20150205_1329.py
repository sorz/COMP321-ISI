# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20150129_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cpu_model',
            field=models.CharField(max_length=127, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='eth_chip',
            field=models.CharField(max_length=127, verbose_name='Ethernet Chip', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='has_usb',
            field=models.BooleanField(default=False, verbose_name='Has USB ports'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='lan_ports',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='No. of LAN ports', default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='lan_speed',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Max LAN Speed', default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='power',
            field=models.CharField(max_length=127, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='wan_ports',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='No. of WAN ports', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='wireless_type',
            field=models.CharField(max_length=127, null=True),
            preserve_default=True,
        ),
    ]
