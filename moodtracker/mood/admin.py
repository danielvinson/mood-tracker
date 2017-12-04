# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from mood.models import *

# Add Profile to the end of the User edit form in Admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserProfileAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number')
    list_select_related = ('profile', )

    def get_phone_number(self, instance):
        return instance.profile.phone_number
    get_phone_number.short_description = 'Phone Number'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserProfileAdmin, self).get_inline_instances(request, obj)

# Display each model correctly in admin
class IncomingSMSAdmin(admin.ModelAdmin):
    pass

class MoodResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_related_user', 'get_related_sms', 'mood', 'get_tone')

    def get_related_user(self, instance):
        if instance.user:
            return instance.user
        else:
            return "No User"
    get_related_user.short_description = "User"

    def get_related_sms(self, instance):
        if instance.related_sms:
            return instance.related_sms
        else:
            return "No Related SMS"
    get_related_sms.short_description = "SMS"

    def get_tone(self, instance):
        if instance.tone:
            return ["%s, %s" % (tone['tone_name'], tone['score']) for tone in json.loads(instance.tone)['document_tone']['tones']]
        else:
            return "No Tone"
    get_tone.short_description = "Tone"


# removed un-customized User
admin.site.unregister(User)

admin.site.register(User, UserProfileAdmin)
admin.site.register(IncomingSMS, IncomingSMSAdmin)
admin.site.register(MoodResponse, MoodResponseAdmin)