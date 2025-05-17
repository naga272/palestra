# Progetto Forum & Library

## Descrizione

Questo progetto è un'applicazione Django che offre sia funzionalità di forum che una libreria di risorse sui linguaggi di programmazione. Include sia il front-end che il back-end, con le seguenti sezioni principali:

1. **Forum**: Gli utenti possono fare domande e rispondere in modo anonimo. È stato implementato un filtro per le parole bannate, gestito attraverso il database. Le parole bannate possono essere visualizzate e modificate tramite l'admin suite di Django oppure direttamente nel database. Ci sono due modi per aggiungere parole bannabili:
    - **Dataset nella cartella flussi**: Inserendo un file con un elenco di parole (una parola per riga) nella cartella `flussi`. Ogni 5 minuti, il server verifica la presenza di nuovi dataset in questa cartella e aggiorna il database di conseguenza.
    - **Admin suite di Django**: Aggiungendo le parole direttamente tramite l'admin suite di Django.


2. **Libreria**: Una raccolta di spiegazioni sui linguaggi di programmazione, accessibile a tutti gli utenti.


## Esecuzione

Per eseguire il progetto, segui questi passaggi:

1. Avvia il file `run.bat` che si trova nella directory `/bin/`. Questo script include due variabili configurabili:
    - `download_lib`: Se impostato a 1, installa le librerie necessarie per l'esecuzione del programma (di default impostato a 1).
    - `debug`: Se impostato a 1, svuota tutte le tabelle del database (di default impostato a 0).

2. Una volta avviato il server, apri un browser e naviga all'indirizzo [127.0.0.1:8000](http://127.0.0.1:8000) per visualizzare il sito in azione.


## Requisiti

Assicurati di avere i seguenti requisiti prima di eseguire il progetto:

- Python 3.x incluso nella PATH.
- Le librerie necessarie elencate nel file `requirements.txt`, installabili con `pip`:
    ```bash
    pip install -r requirements.txt
    ```
- Un browser web moderno.


## Struttura del Progetto

- `/bin/`: Contiene lo script `run.bat`, database e gli script python che consentono l'avvio del progetto.
- `/flussi/`: Cartella dove inserire i dataset con le parole bannabili. Le parole devono essere elencate una per riga
- `/static/`: contiene file CSS, JS e immagini.
- `/templates/`: contiene file HTML.


## author

- Braga Mattia
- Bastianello Federico
