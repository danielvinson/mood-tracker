# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 00:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0004_moodresponse_tone'),
    ]

    operations = [
        migrations.AddField(
            model_name='moodresponse',
            name='related_sms',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mood.IncomingSMS'),
        ),
    ]
