# mood-tracker
Service which allows you to track how you are feeling via SMS.  Set a schedule for reminders, then respond to each text (or text whenever you want) with how you are feeling in real words and/or a number.  This service will record your responses and analyze them to provide a detailed history.

Backend: Django, SQLite3, RabbitMQ, Celery

* CeleryBeat with RabbitMQ broker is used to create scheduled text messages.

Frontend: React, NVD3 (using react-nvd3).

* Transformed in-browser using babel-standalone.
* Still using Django templates and url routing.

External Services: Twilio, IBM Watson Tone Analyzer

* Twilio handles SMS send/recieve
* All recieved messages get processed through the Tone Analyzer API, and the resulting data is stored for that time.



Deploy instructions: (on an Ubuntu EC2 instance)

echo 'deb http://www.rabbitmq.com/debian/ testing main' |
     sudo tee /etc/apt/sources.list.d/rabbitmq.list

sudo apt-get update

sudo apt-get install python2.7 python-pip rabbitmq-server

sudo git clone https://github.com/danielvinson/mood-tracker.git

cd moodtracker

sudo pip install -r requirements.txt

sudo python manage.py createsuperuser (follow prompts)

sudo python manage.py supervisor
