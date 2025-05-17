@echo off

REM installazione librerie python - settare 1 per il si, 0 per no
set /A download_lib = 0

REM RESETTO IL DB OGNI VOLTA IN FASE DI TEST (settato a 0 non lo fa)
set /A debug = 0

REM server project public (setta a 1 se vuoi che il progetto diventi visibile anche esternamente)
set /A spp = 0

if %download_lib% == 1 pip install -r ../requirements.txt 

REM ATTENZIONE!
if %debug% == 1 python manage.py flush
if %debug% == 1 python manage.py makemigrations
if %debug% == 1 python manage.py migrate


REM python manage.py runserver 0.0.0.0:8000 pubblica online il server
if %spp% == 0 python manage.py runserver else python manage.py runserver 0.0.0.0:80
