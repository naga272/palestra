# Implementazione esame di maturita di INI

## Descrizione

Leggi il file "Simulazione_seconda_prova_28042025.docx".
Oltre a questo, Ho aggiunto la possibilità per il negozio di aggiungere prodotti.
NB: non è stato aggiunto css e js al progetto, non è stato implementato il messaggio via email con QR Code


## Esecuzione

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Se si vuole pubblicare:

```bash
python manage.py runserver 0.0.0.0:8000
```

NB: setta il flag in settings.py DEBUG = False

## Requisiti

- python > 3.12
- visualizza requirements.txt per vedere quali librerie sono necessarie

## author

- naga272
