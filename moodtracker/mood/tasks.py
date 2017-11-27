from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.contrib.auth.models import User

from mood import util

# Celery task file - defines tasks which can be run asyncronously or on timers

@shared_task
def ask_for_mood(user_id):
    try:
        user = User.objects.get(id=user_id)
        if not user.profile.is_verified:
            return "User not verified - not sending SMS"
        pn = user.profile.phone_number
        message = "How are you feeling?"
        msg = util.send_sms(pn, message)
        return True
    except Exception, e:
        return e