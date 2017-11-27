# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import re

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from mood import util

#####
#
#   Profile
#
####

class Profile(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number        = models.CharField(max_length=12, blank=True)
    is_verified         = models.BooleanField(default=False)
    schedule_enabled    = models.BooleanField(default=False)
    # Schedule object is unique for this User so we can not worry about deleting them.
    # Schedules will be editable
    schedule            = models.OneToOneField(CrontabSchedule, on_delete=models.CASCADE, blank=True, null=True)
    # Task is an object that will not be directly editable
    task                = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal to create Profile, Schedule, and Task when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        s = CrontabSchedule.objects.create(
            minute='0',
            hour='*',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )
        t = PeriodicTask.objects.create(
            crontab=s,
            name=instance.username,
            task='mood.tasks.ask_for_mood',
            args=json.dumps([instance.id]),
        )
        Profile.objects.create(user=instance, schedule=s, task=t)

# Signal to update Profile when User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.schedule.save()
    instance.task.save()

#####
#
#   SMS
#
####

class IncomingSMS(models.Model):
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number    = models.CharField(max_length=12)
    message         = models.CharField(max_length=160)
    timestamp       = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.message

# Signal to trigger when we save any SMS associated with a User into the DB
@receiver(post_save, sender=IncomingSMS)
def process_incoming_sms(sender, instance, **kwargs):
    isms = instance
    user = instance.user
    # Look at numbers for numerical mood
    mood = re.sub(r'[^0-9]', '', isms.message)
    if mood == '':
        mood = 0
    # Look at full message for tone
    tone = json.dumps(util.get_tone(isms.message))
    MoodResponse.objects.create(
        user=user,
        related_sms=isms,
        mood=mood,
        tone=tone,
    )

class MoodResponse(models.Model):
    # Used for storing Mood Responses
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    related_sms     = models.ForeignKey(IncomingSMS, on_delete=models.SET_NULL, blank=True, null=True)
    mood            = models.IntegerField(blank=False)
    timestamp       = models.DateTimeField(default=timezone.now)
    tone            = models.TextField(max_length=5000, blank=True, null=True)
    
    def __str__(self):
        return "%s - %s @ %s" % (self.user, self.mood, self.timestamp.strftime('%Y-%m-%d %H:%M'))