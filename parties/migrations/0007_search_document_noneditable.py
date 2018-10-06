# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-10-06 20:13
from __future__ import unicode_literals

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0006_merge_20180419_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='search_document',
            field=django.contrib.postgres.search.SearchVectorField(editable=False, null=True),
        ),
    ]
