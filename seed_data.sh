#!/bin/bash

rm -rf practicepalapi/migrations
rm db.sqlite3
python manage.py makemigrations practicepalapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata appusers
python manage.py loaddata instruments
python manage.py loaddata songs
python manage.py loaddata sections
python manage.py loaddata attempts
python manage.py loaddata competitions
