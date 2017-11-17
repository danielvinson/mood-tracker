# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from mood.forms import SignUpForm
from mood.models import IncomingSMS, Profile
from mood import util

# Create your views here.

def index(request):
    return HttpResponse("Hello, world")

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
    return render(request, 'signup.html', {'form': form})

def incoming_sms(request):
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
    util.send_sms(origin_number, 'Thanks!')
    return HttpResponse('Success', content_type='text/plain')
