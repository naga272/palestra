#!/bin/bash

rm ./db.sqlite3 ./app/migrations/0001_initial.py

python manage.py makemigrations
python manage.py migrate
python manage.py shell < ./scripts/popolamento.py
