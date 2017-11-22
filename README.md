# mood-tracker
Service which allows you to track your mood via SMS


Backend: Django, SQLite3

Frontend: Currenly MVP using jQuery.  Will move to React soon.

External Services: Twilio, IBM Watson Tone Analyzer





Deploy instructions (on EC2):

sudo apt-get install python2.7 python-pip

sudo git clone https://github.com/danielvinson/mood-tracker.git

cd moodtracker

sudo pip install -r requirements.txt

sudo python manage.py createsuperuser

sudo python manage.py runserver 0.0.0.0:80
