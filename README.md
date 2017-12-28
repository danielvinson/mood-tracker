# mood-tracker
Service which allows you to track how you are feeling via SMS.  Set a schedule for reminders, then respond to each text (or text whenever you want) with how you are feeling in real words and/or a number.  This service will record your responses and analyze them to provide a detailed history.

Screenshots:

![Moodtracker1](/screenshots/mt-1.png?raw=true)
![Moodtracker2](/screenshots/mt-2.png?raw=true)
![Moodtracker3](/screenshots/mt-3.png?raw=true)

Backend: Django, SQLite3, RabbitMQ, Celery

* CeleryBeat with RabbitMQ broker is used to create scheduled text messages.

Frontend: React, NVD3 (using react-nvd3).

* Transformed in-browser using babel-standalone.
* Still using Django templates and url routing.

External Services: Twilio, IBM Watson Tone Analyzer

* Twilio handles SMS send/recieve
* All recieved messages get processed through the Tone Analyzer API, and the resulting data is stored for that time.


Current To-Do List:

* Fix UI for managing profile schedules.  Plan is to use common presets with a "custom" option.
* Profile images support.
* Functions for converting MoodResponse's time into a more managable format.  I'm thinking that a good strategy here (outside of the obvious of "use a time-series database") is to choose a time granularity as a profile option, then round all MoodResponses to the nearest point in that.  For example an hourly granularity would round to the nearest hour in the process when converting from IncomingSMS to MoodResponse.  Handling multiple data-points at the same time might be a non-issue.


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


Some notes on development/design process:

Scheduling:

There are a bunch of ways to implement scheduled events.  

I chose to go with Celery+RabbitMQ over a Daemon-based solution or other systems because:

* I can use configuration+scripts to very opaquely control the backend, as opposed to using code which would be hard to maintain or understand for anybody who is not intimately familiar with the implementation I chose.
* Using one tasks.py file is very easily maintainable and is very DRY.
* Changing schedules for one user doesn't effect the other users.
* All schedules can be easily stored in the Django database with almost no changes.
* Crontabs are a known thing which are sometimes hard to work with, but are a known quantity.


