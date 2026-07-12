import time
import random
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from app.models import (
    BaseDataUser, Azienda, Filiale, SupervisoreAzienda,
    Progetto, Studente, Proff, Diario, PaginaDiario
)

# Pulisce i dati precedenti
PaginaDiario.objects.all().delete()
Diario.objects.all().delete()
Studente.objects.all().delete()
Progetto.objects.all().delete()
SupervisoreAzienda.objects.all().delete()
Filiale.objects.all().delete()
Azienda.objects.all().delete()
Proff.objects.all().delete()
BaseDataUser.objects.all().delete()

print("Database svuotato, inizio popolamento...")

# --- Crea aziende ---
aziende_data = [
    ("ITech Solutions", "12345678901", "Sviluppo software e consulenza tecnologica"),
    ("GreenLog S.p.A.", "98765432109", "Logistica sostenibile e trasporti"),
    ("EduForma SRL", "11122334455", "Formazione aziendale e servizi educativi"),
]

aziende = []
for nome, piva, descrizione in aziende_data:
    aziende.append(Azienda.objects.create(nome=nome, piva=piva, descrizione=descrizione))

# --- Filiali ---
filiali = [
    Filiale.objects.create(azienda=aziende[0], via="Via Roma", n_civico="12", comune="Torino", citta="Torino"),
    Filiale.objects.create(azienda=aziende[1], via="Via Milano", n_civico="45B", comune="Genova", citta="Genova"),
    Filiale.objects.create(azienda=aziende[2], via="Corso Italia", n_civico="7", comune="Firenze", citta="Firenze"),
]

# --- Supervisori ---
sup_utenti = [
    ("supv_mario", "Mario", "Rossi"),
    ("supv_luca", "Luca", "Bianchi"),
    ("supv_paolo", "Paolo", "Verdi"),
]

supervisori = []
for i, (username, nome, cognome) in enumerate(sup_utenti):
    u = BaseDataUser.objects.create_user(
        username=username,
        password="test123",
        first_name=nome,
        last_name=cognome,
        email="bastianellofederico4@gmail.com",
        ruolo="SUPV",
        codFiscale=f"RSSMRA{i+1:02d}A01H501X",
        DataNascita="1980-05-12"
    )
    supervisori.append(SupervisoreAzienda.objects.create(user=u, filiale=filiali[i]))

# --- Progetti ---
now = time.time()
progetti = [
    Progetto.objects.create(
        supervisore=supervisori[0],
        titolo="Sistema di gestione interna",
        descrizione="Sviluppo di un portale interno per l’azienda.",
        requisiti="Python, Django, HTML, CSS",
        tempo_stimato=180,
        n_posti_disp=2,
        is_completato=False,
        timestamp_creazione=now - 86400 * 5  # 5 giorni fa
    ),
    Progetto.objects.create(
        supervisore=supervisori[1],
        titolo="Ottimizzazione logistica",
        descrizione="Analisi dei flussi e miglioramento della catena di trasporto.",
        requisiti="Excel, SQL, capacità analitiche",
        tempo_stimato=120,
        n_posti_disp=5,
        is_completato=False,
        timestamp_creazione=now - 86400 * 8
    ),
    Progetto.objects.create(
        supervisore=supervisori[2],
        titolo="Piattaforma e-learning",
        descrizione="Creazione di una piattaforma formativa per corsi online.",
        requisiti="React, Django REST, UX/UI",
        tempo_stimato=200,
        n_posti_disp=5,
        is_completato=False,
        timestamp_creazione=now - 86400 * 3
    ),
]

# --- Professori ---
prof_utenti = [
    ("prof_giulia", "Giulia", "Ferrari"),
    ("prof_lorenzo", "Lorenzo", "Conti"),
]
proff = []
for username, nome, cognome in prof_utenti:
    u = BaseDataUser.objects.create_user(
        username=username,
        password="test123",
        first_name=nome,
        last_name=cognome,
        email="bastianellofederico4@gmail.com",
        ruolo="PROF",
        codFiscale=f"FRRGLL{random.randint(10, 99)}A01H501F",
        DataNascita="1975-03-21"
    )
    proff.append(Proff.objects.create(user=u))


# --- Studenti ---
studenti_data = [
    ("studente1", "Andrea", "Gallo", "S001", 5, "A", 120, progetti[0]),
    ("studente2", "Chiara", "Esposito", "S002", 5, "B", 100, progetti[1]),
    ("studente3", "Davide", "Romano", "S003", 5, "C", 80, progetti[2]),
]


studenti = []
for username, nome, cognome, matricola, anno, sez, ore, progetto in studenti_data:
    u = BaseDataUser.objects.create_user(
        username=username,
        password="test123",
        first_name=nome,
        last_name=cognome,
        email="bastianellofederico4@gmail.com",
        ruolo="STUD",
        codFiscale=f"GLLAND{random.randint(10,99)}A01H501Z",
        DataNascita="2007-11-10"
    )
    s = Studente.objects.create(
        user=u,
        progetto=progetto,
        timestamp_presa_incarico_p=time.time(),
        matricola=matricola,
        anno_scolastico=anno,
        sezione=sez,
        tot_ore_pcto=ore
    )
    studenti.append(s)

# --- Diari e Pagine ---
for studente, prof in zip(studenti, proff * 2):  # associa ciclicamente i professori
    diario = Diario.objects.create(studente=studente, professore=prof)
    for i in range(2):
        PaginaDiario.objects.create(
            diario=diario,
            supervisore=studente.progetto.supervisore,
            contenuto=f"Resoconto giorno {i+1}: attività di {studente.user.first_name}.",
            data=make_aware(datetime.now() - timedelta(days=i))
        )

print("Popolamento completato con successo.")
