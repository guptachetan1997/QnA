# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-18 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='anonymous',
            field=models.BooleanField(default=0),
        ),
    ]
