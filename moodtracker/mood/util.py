import requests
from requests.auth import HTTPBasicAuth
import json


from moodtracker.settings import BLUEMIX_USERNAME, BLUEMIX_PASSWORD

def get_tone(text):
    url_base = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21'
    p = {'text': text}
    r = requests.get(url_base, params=p, auth=HTTPBasicAuth(BLUEMIX_USERNAME,BLUEMIX_PASSWORD))
    return r.json()