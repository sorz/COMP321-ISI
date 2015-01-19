# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('S', 'Shipping'), ('R', 'Received'), ('H', 'Hold'), ('C', 'Cancelled')], max_length=1, default='P')),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('shipment_date', models.DateTimeField(null=True)),
                ('recipient_name', models.CharField(max_length=255)),
                ('recipient_address', models.CharField(max_length=255, verbose_name='address')),
                ('recipient_address_2', models.CharField(max_length=255, blank=True, verbose_name='address (2th line)')),
                ('recipient_postcode', models.CharField(max_length=63, blank=True, verbose_name='zip')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(validators=[django.core.validators.MinValueValidator(0)], decimal_places=2, max_digits=9)),
                ('order', models.ForeignKey(to='order.Order')),
                ('product', models.ForeignKey(to='product.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='order',
            field=models.ForeignKey(to='order.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='writer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
