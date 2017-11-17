# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from twilio.twiml.messaging_response import MessagingResponse, Message

from mood.models import IncomingSMS, MoodUser

# Create your views here.

def index(request):
    return HttpResponse("Hello, world")

def incoming_sms(request):
    origin_number = request.POST.get('From','')
    message = request.POST.get('Body','')
    user = MoodUser.objects.filter(phone_number=origin_number)
    if user:
        user = user[0]
    else:
        user = None
    isms = IncomingSMS(phone_number=origin_number, message=message, user=user)
    isms.save()
    twiml = '<Response><Message>Thanks for your response!</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')
