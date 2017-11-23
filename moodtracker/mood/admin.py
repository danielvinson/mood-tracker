# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mood.models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(IncomingSMS)
admin.site.register(MoodResponse)