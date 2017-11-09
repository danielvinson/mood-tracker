# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from twilio.twiml.messaging_response import MessagingResponse


# Create your views here.

def index(request):
    return HttpResponse("Hello, world")

def incoming_sms(request):
    twiml = '<Response><Message>Thanks for your response!</Message></Response>'
    return HttpResponse(twiml, content_type='text/xml')
