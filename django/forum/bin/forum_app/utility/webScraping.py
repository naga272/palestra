from    typing      import Tuple
from    bs4         import BeautifulSoup
import  pandas      as pd
import  requests


def web_scraping(url: str, class_for_identify: str) -> list[str] | None:
    """
    * Funzione che data analizza una tabella di una pagina web e ne estrae il contenuto.
    * @url: link pagina web
    * @class_for_identify: classi del FE della tabella
    *
    * resituisce due liste:
    * @headers: contiene l'intestazione della tabella
    * @data: contiene il body della tabella html
    *
    * Nel caso in cui non è riuscito a mandare la richiesta restituisce None,
    * loggando l'evento nel trace.db.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Questo solleverà un'eccezione se la richiesta non ha successo

    except requests.exceptions.HTTPError as http_err:
        Log().logMe(f"errore nel tentativo di mandare una richiesta alla pagina {url}. Tipo errore:{http_err}")
        return None, None

    soup = BeautifulSoup(response.content, "html.parser")               # Analizza il contenuto della pagina
    tables = soup.find_all("table", {"class": class_for_identify})      # Trova tutte le tabelle con la classe desiderata
    table = tables[0] 
    headers = [header.text.strip() for header in table.find_all("th")]  # Estraggo l'intestazione della tabella
    rows = table.find_all("tr")[1:]                                     # Estraggo tutte le righe della tabella tranne l'intestazione

    data = [] # lista vuota per contenere i dati estratti

    for row in rows:
        cells = row.find_all(["td", "th"])                  # Estrarre tutte le celle della riga
        row_data = [cell.text.strip() for cell in cells]    # Estrai il testo da ogni cella, rimuovi spazi e aggiungi alla lista
        row_text = " ".join(row_data)                       # Unisci i dati della riga in una stringa separata da spazi
        data.append(row_text)                               # Aggiungi la riga alla lista dei dati

    return headers, data 
