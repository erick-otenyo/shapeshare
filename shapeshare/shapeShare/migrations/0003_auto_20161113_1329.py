# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-13 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shapeShare', '0002_auto_20161113_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100),
        ),
    ]