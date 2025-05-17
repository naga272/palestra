
from    sqlalchemy      import create_engine, inspect, Column, Integer, String, Float, MetaData, Table
from    sqlalchemy.orm  import sessionmaker, declarative_base

from    bs4             import BeautifulSoup
from    log             import Log
import  chardet     # usata per detect_encoding_file
import  bcrypt
import  time
import  re
import  os


n_richieste = [] # NB: variabile che deve essere visibile solo a questo modulo, viene usata nella funzione client_request()


def detect_encoding_file(file_path: str) -> str:
    # funzione che identifica l'encoding di file_path  
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result["encoding"]


def paragona(testo: str, ban_word: set) -> str:
    """
    * Funzione che verifica se all'intenro della stringa testo sono contenute determinate parole.
    * Nel caso in cui vengano trovate restituisce la stringa True, altrimenti restituisce False.
    * @testo: un testo scritto da un utente
    * @ban_word: oggetto 'django.db.models.query.QuerySet' (contiene la lista delle parole non consentite dal db) 
    """
    testo = testo.upper()
    for word in ban_word:
        if word.word.upper() in testo:
            return True

    return False


def client_request(matricola: str) -> str:
    """
    * Per motivi di sicurezza ogni client può mandare un massimo di 5 richieste al minuto.
    * Questa funzione tramite la lista n_richieste, controlla se la stessa matricola
    * manda più di 5 richieste al minuto. restituisce valore "va bene" se il client non supera questo limite,
    * altrimenti darà "troppi tentativi per singola matricola".
    *
    * @matricola: la matricola che identifica il singolo studente
    """
    global n_richieste

    max_requests_per_minute = 3
    time_window_seconds = 60
    current_time = time.time()

    # n_richieste rimuove richieste più vecchie di 60 secondi
    n_richieste = [req for req in n_richieste if current_time - req[1] <= time_window_seconds]

    # Contatore di numero richieste dallo stesso client
    counter = sum(1 for req in n_richieste if req[0] == matricola)

    if counter < max_requests_per_minute:
        n_richieste.append((matricola, current_time))
        return "va bene"
    else:
        Log().logMe(f"Errore - la matricola {matricola} sta facendo troppe richieste, contatore: {counter}!")
        return "troppi tentativi per singola matricola"


def content_changelog() -> str:
    # funzione che restituisce tutto il contenuto del changelog -> serve per la homepage del FE
    return open("../CHANGELOG.txt", "r", encoding=detect_encoding_file("../CHANGELOG.txt")).read()


def last_version(cng: str) -> str:
    """
    *   Funzione che analizza il changelog per capire a che versione siamo (la versione del programma la uso per il log).
    """
    with open(cng, "r") as analizza:
        for row in analizza:
            if re.match(r"\s*##\s*version.*\n*", row):
                parts = row.split("[")
                return parts[1].split("]")[0]     # la versione che si trova più in alto è la maggiore


'''
Per il Forum in futuro (ancora in fase di sviluppo):
import Levenshtein

# dataset insulti
insulti = ['stonzo', 'idiota', 'cretino', 'buffone', "coglione"]

def rilevatoreInsulti(parola, soglia=2):
    for insulto in insulti:
        distanza = Levenshtein.distance(parola, insulto)
        if distanza <= soglia:
            return f"Insulto rilevato: '{insulto}' (distanza: {distanza})"
    return "Nessun insulto rilevato."


# Esempi di parole da controllare
checkWords = ['st0nz0', 'id3ota...', 'bufoon', "col1one"]
'''
