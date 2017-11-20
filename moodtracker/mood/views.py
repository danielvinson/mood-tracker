# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from mood.forms import SignUpForm
from mood.models import IncomingSMS, Profile, MoodPoint
from mood import util

#####
#
#       Front-End Views
#
######

def index(request):
    return render(request, 'index.html')

def profile(request, username):
    u = User.objects.get(username=username)
    p = u.profile
    return render(request, 'user/profile.html', {'user': model_to_dict(u), 'profile': model_to_dict(p)})

def mood_history(request):
    return render(request, 'user/mood_history.html')

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

def user_data(request):
    # Returns data from the database for the specified user.
    if request.method == 'GET':
        user_id = request.GET.get('user_id','')
        text_history_start = request.GET.get('text_start','')
        text_history_end = request.GET.get('text_end','')
        mood_history_start = request.GET.get('mood_start','')
        mood_history_end = request.GET.get('mood_end','')
        data = {}
        if user_id:
            user = User.objects.get(id=user_id)
            data['user'] = model_to_dict(user)
            data['profile'] = model_to_dict(user.profile)
            ####
            isms = IncomingSMS.objects.filter(user=user)
            data['texts'] = []
            for msg in isms:
                data['texts'].append(model_to_dict(msg))
            ####
            mps = MoodPoint.objects.filter(user=user)
            data['mood'] = []
            for mp in mps:
                data['mood'].append(model_to_dict(mp))
        return HttpResponse(json.dumps(data, indent=4, default=str), content_type='text/json')
