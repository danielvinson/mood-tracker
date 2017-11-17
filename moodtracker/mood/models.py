# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class MoodUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)

class IncomingSMS(models.Model):
    user = models.ForeignKey(MoodUser, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=12)
    message = models.CharField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
