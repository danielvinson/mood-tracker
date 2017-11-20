# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number    = models.CharField(max_length=12, blank=True)
    is_verified     = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# Signal to create profile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to update Profile when user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class IncomingSMS(models.Model):
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number    = models.CharField(max_length=12)
    message         = models.CharField(max_length=160)
    timestamp       = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.timestamp.strftime('%Y-%m-%d %H:%M'))

class MoodPoint(models.Model):
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    mood            = models.IntegerField()
    timestamp       = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "%s - %s @ %s" % (self.user, self.mood, self.timestamp.strftime('%Y-%m-%d %H:%M'))