# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from mood import util
from mood.forms import SignUpForm
from mood.models import IncomingSMS, Profile, MoodResponse

#####
#
#       Front-End Views
#
######

def index(request):
    return render(request, 'index.html')

def profile(request, username):
    u = User.objects.get(username=username)
    return render(request, 'user/profile.html', {'user_id': u.id})

@login_required(login_url='/moodtracker/login/')
def settings(request, username):
    u = User.objects.get(username=username)
    return render(request, 'user/settings.html', {'user_id': u.id})

@login_required(login_url='/moodtracker/login/')
def mood(request, username):
    u = User.objects.get(username=username)
    return render(request, 'user/mood.html', {'user_id': u.id})

#####
#
#     Registration/Auth Views
#
######

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

#####
#
#	APIs
#
######

def incoming_sms(request):
    # API endpoint for Twilio webhooks.
    # When Twilio POSTs us the data of an incoming message,
    # we add that data to our database, then repond via Twilio.
    origin_number = request.POST.get('From','')
    message = request.POST.get('Body','')
    try:
        profile = Profile.objects.get(phone_number=origin_number)
        user = profile.user
    except Exception, e:
        # We could throw an error here, but I want to
        # record incoming texts which aren't from a user
        user = None
    isms = IncomingSMS(phone_number=origin_number, message=message, user=user)
    isms.save()
    # Send response message
    return HttpResponse('Thanks!', content_type='text/plain')

@login_required(login_url='/moodtracker/login/')
def get_user_data(request):
    # Returns data from the database for the specified user.
    # Permission = only self
    if request.method == 'GET':
        user_id = request.GET.get('user_id','')
        #if not request.user.id == int(user_id):  turned off for testing
            #raise PermissionDenied
        text_history_start = request.GET.get('text_start','')
        text_history_end = request.GET.get('text_end','')
        mood_history_start = request.GET.get('mood_start','')
        mood_history_end = request.GET.get('mood_end','')
        data = {}
        if user_id:
            user = User.objects.get(id=user_id)
            ####
            data['texts'] = []
            for msg in IncomingSMS.objects.filter(user=user):
                data['texts'].append(model_to_dict(msg))
            ####
            data['mood'] = []
            for mr in MoodResponse.objects.filter(user=user):
                mood = model_to_dict(mr)
                # Convert tone from JSON string -> object
                if mood['tone']:
                    mood['tone'] = json.loads(mood['tone'])
                else:
                    mood['tone'] = ''
                data['mood'].append(mood)
            ####
        return HttpResponse(json.dumps(data, indent=4, default=str), content_type='text/json')

@login_required(login_url='/moodtracker/login/')
def get_user_profile(request):
    # Returns public profile data
    # Permission = any logged in user
    if request.method == 'GET':
        user_id = request.GET.get('user_id','')
        data = {}
        if user_id:
            user = User.objects.get(id=user_id)
            # Manually making a dict with the results because there is a lot of internal
            # information stored in the user object which we don't want available.
            data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.profile.phone_number,
                'is_verified': user.profile.is_verified,
                'schedule_enabled': user.profile.schedule_enabled,
                'schedule_minute': user.profile.schedule.minute,
                'schedule_hour': user.profile.schedule.hour,
                'schedule_day_of_month': user.profile.schedule.day_of_month,
                'schedule_day_of_week': user.profile.schedule.day_of_week,
                'schedule_month_of_year': user.profile.schedule.month_of_year, 
            }
        return HttpResponse(json.dumps(data, indent=4, default=str), content_type='text/json')

@login_required(login_url='/moodtracker/login/')
def update_user_profile(request):
    # Allows a user to update their profile
    # Params:
    #    user_id == the user to be changed
    #    key=value to change user
    if request.method == 'GET':
        user_id = request.GET.get('user_id','')
        if not request.user.id == int(user_id):
            raise PermissionDenied
        ###
        user = User.objects.get(id=user_id)
        ## User
        if request.GET.get('username',''):
            user.username = request.GET.get('username','')
            user.save()
        if request.GET.get('email',''):
            user.email = request.GET.get('email','')
            user.save()
        if request.GET.get('first_name',''):
            user.first_name = request.GET.get('first_name','')
            user.save()
        if request.GET.get('last_name',''):
            user.last_name = request.GET.get('last_name','')
            user.save()
        ## Profile
        if request.GET.get('phone_number', ''):
            user.profile.phone_number = request.GET.get('phone_number','')
            user.profile.save()
        if request.GET.get('schedule_enabled',''):
            user.profile.schedule_enabled = util.str_to_bool(request.GET.get('schedule_enabled',''))
            user.profile.save()
        ## Schedule
        if request.GET.get('schedule_minute',''):
            user.profile.schedule.schedule_minute = request.GET.get('schedule_minute','')
            user.profile.schedule.save()
        if request.GET.get('schedule_hour',''):
            user.profile.schedule.schedule_hour = request.GET.get('schedule_hour','')
            user.profile.schedule.save()
        if request.GET.get('schedule_month_of_year',''):
            user.profile.schedule.schedule_month_of_year = request.GET.get('schedule_month_of_year','')
            user.profile.schedule.save()
        if request.GET.get('schedule_day_of_week',''):
            user.profile.schedule.schedule_day_of_week = request.GET.get('schedule_day_of_week','')
            user.profile.schedule.save()
        if request.GET.get('schedule_day_of_month',''):
            user.profile.schedule.schedule_day_of_month = request.GET.get('schedule_day_of_month','')
            user.profile.schedule.save()
        return HttpResponse("Success!")