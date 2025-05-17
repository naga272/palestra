#!/bin/bash

# Installazione librerie python - settare 1 per il si, 0 per no
download_lib=0

# RESETTO IL DB OGNI VOLTA IN FASE DI TEST
debug=0

if [ $download_lib -eq 1 ]; then
    pip install -r ../requirements.txt
fi

# ATTENZIONE!
if [ $debug -eq 1 ]; then
    python3 manage.py flush
    python3 manage.py collectstatic
fi

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:80
