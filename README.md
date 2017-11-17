# mood-tracker
Service which allows you to track your mood via SMS


Backend: Django, Postgres

Frontend: React

External Services: Twilio, IBM Watson Tone Analyzer



Deploy instructions:

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install python2.7

sudo apt-get install python-pip

sudo pip install django

sudo pip install requests

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt-get install wget ca-certificates

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install postgresql-9.6 pgadmin3

