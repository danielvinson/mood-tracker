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
def mood(request):
    return render(request, 'user/mood.html')

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
    return HttpResponse('Success', content_type='text/plain')

@login_required(login_url='/moodtracker/login/')
def get_user_data(request):
    # Returns data from the database for the specified user.
    # Permission = only self
    if request.method == 'GET':
        user_id = request.GET.get('user_id','')
        if not request.user.id == int(user_id):
            raise PermissionDenied
        text_history_start = request.GET.get('text_start','')
        text_history_end = request.GET.get('text_end','')
        mood_history_start = request.GET.get('mood_start','')
        mood_history_end = request.GET.get('mood_end','')
        data = {}
        if user_id:
            user = User.objects.get(id=user_id)
            ####
            isms = IncomingSMS.objects.filter(user=user)
            data['texts'] = []
            for msg in isms:
                data['texts'].append(model_to_dict(msg))
            ####
            mps = MoodResponse.objects.filter(user=user)
            data['mood'] = []
            for mp in mps:
                data['mood'].append(model_to_dict(mp))
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
                'is_staff': user.is_staff, # Add a link to admin? there's a use here
                'schedule_minute': user.profile.schedule.minute,
                'schedule_hour': user.profile.schedule.hour,
                'schedule_day_of_month': user.profile.schedule.day_of_month,
                'schedule_day_of_week': user.profile.schedule.day_of_week,
                'schedule_month_of_year': user.profile.schedule.month_of_year                
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
        if request.GET.get('username',''):
            user.username = request.GET.get('username','')
        if request.GET.get('email',''):
            user.email = request.GET.get('email','')
        if request.GET.get('first_name',''):
            user.first_name = request.GET.get('first_name','')
        if request.GET.get('last_name',''):
            user.last_name = request.GET.get('last_name','')
        if request.GET.get('phone_number', ''):
            user.profile.phone_number = request.GET.get('phone_number','')
        ###
        user.save()
        return HttpResponse("Success!")