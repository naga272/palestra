
from django.contrib import admin
from .models import (
    BaseDataUser, 
    Diario, Azienda, Progetto,
    Studente, SupervisoreAzienda, Proff,
    Filiale
)


all_class_model = [
    BaseDataUser,
    Diario, Azienda, Progetto,
    Studente, SupervisoreAzienda, Proff,
    Filiale
]


for element in all_class_model:
    admin.site.register(element)
