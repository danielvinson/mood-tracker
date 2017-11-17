# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from twilio.twiml.messaging_response import MessagingResponse, Message

from mood.models import IncomingSMS, Profile
from mood import util

# Create your views here.

def index(request):
    return HttpResponse("Hello, world")

def incoming_sms(request):
    origin_number = request.POST.get('From','')
    message = request.POST.get('Body','')
    try:
        profile = Profile.objects.get(phone_number=origin_number)
        user = profile.user
    except Exception, e:
        user = None
        print e
    isms = IncomingSMS(phone_number=origin_number, message=message, user=user)
    isms.save()
    # Send response message
    util.send_sms(origin_number, 'Thanks!')
    return HttpResponse('Success', content_type='text/plain')
