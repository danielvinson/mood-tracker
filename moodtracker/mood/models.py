# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class MoodUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=9)
