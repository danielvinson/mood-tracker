# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-17 18:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingsms',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='mooduser',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
    ]
