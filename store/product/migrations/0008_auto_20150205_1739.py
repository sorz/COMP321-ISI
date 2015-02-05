# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20150205_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cpu_model',
            field=models.CharField(max_length=127, blank=True, verbose_name='CPU model'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='eth_chip',
            field=models.CharField(max_length=127, blank=True, verbose_name='Ethernet chip'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='lan_speed',
            field=models.IntegerField(verbose_name='Max LAN speed', validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Product name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, verbose_name='Price ($)', max_digits=9, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='wireless_type',
            field=models.CharField(max_length=127, blank=True, default=''),
            preserve_default=False,
        ),
    ]
