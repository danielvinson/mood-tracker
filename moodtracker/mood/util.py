import requests
from requests.auth import HTTPBasicAuth
import json

from moodtracker.settings import BLUEMIX_USERNAME, BLUEMIX_PASSWORD, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER
from twilio.rest import Client

def get_tone(text):
    url_base = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21'
    p = {'text': text}
    r = requests.get(url_base, params=p, auth=HTTPBasicAuth(BLUEMIX_USERNAME,BLUEMIX_PASSWORD))
    return r.json()

def verify_sms_number():
    pass

def send_sms(phone_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(to=phone_number, from_=TWILIO_NUMBER, body=message)
    return message
