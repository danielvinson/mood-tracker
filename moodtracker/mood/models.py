# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

#####
#
#   Profile
#
####

class Profile(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number        = models.CharField(max_length=12, blank=True)
    is_verified         = models.BooleanField(default=False)
    schedule            = models.OneToOneField(CrontabSchedule, on_delete=models.CASCADE, blank=True, null=True)
    task                = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, blank=True, null=True)
    schedule_enabled    = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Signal to create profile when a User is created
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
        )
        Profile.objects.create(user=instance, schedule=s, task=t)

# Signal to update Profile when user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.schedule.save()
    instance.profile.task.save()
    instance.profile.save()

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
        return "%s - %s" % (self.user, self.timestamp.strftime('%Y-%m-%d %H:%M'))

class MoodResponse(models.Model):
    # Used for storing Mood Responses
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    mood            = models.IntegerField(blank=False)
    timestamp       = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "%s - %s @ %s" % (self.user, self.mood, self.timestamp.strftime('%Y-%m-%d %H:%M'))