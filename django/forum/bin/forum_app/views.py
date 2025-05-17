
from django.views.decorators.http           import require_http_methods
from django.shortcuts                       import render, redirect
from django.http                            import HttpResponse, JsonResponse
from django.core.files                      import File
from django.core.paginator                  import Paginator                # usato per l'impaginazione del forum
from django.contrib                         import messages                 # Per gestire i messaggi di feedback
from django.views.decorators.csrf           import csrf_exempt

# usato per le richieste a campus
from requests.packages.urllib3.exceptions   import InsecureRequestWarning
from requests.exceptions                    import RequestException

from .models                                import MemoryDomande, MemoryRisposte, BanWord
from .forms                                 import FormDomanda, FormRisposta
from dotenv                                 import load_dotenv
load_dotenv()


"""
*   Ho scomposto il modulo utility.py in più file per tenere tutto il più ordinato possibile.
*   Penso che se teniamo utility.py come unico file che contiene tutto più avanti quando le cose aumenteranno 
*   diventerà più difficile da gestire
*   - general.py:       funzioni di uso generale (match encoding file, match banWord etc...)
*   - chatBot.py:       Gestione e logging delle conversazioni utente-bot (il logging penso che ci consentirà di migliorare il prompt)
*   - webScraping.py:   prelievo di dati da terze parti
*   - encription.py     Criptazione dei dati
"""
from .utility.general                       import paragona, client_request, content_changelog, detect_encoding_file
from .utility.chatBot                       import Model, LogBot
from .utility.webScraping                   import web_scraping
from .utility.encription                    import Security
from datetime                               import datetime
from log                                    import Log

import matplotlib.pyplot                    as plt
import pandas                               as pd
import requests
import asyncio
import json
import re
import os


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def errno_404(request, exception):          # per visualizzare questa pagina settare DEGUB a False
    """
    * Funzione che si attiva quando una pagina web non viene trovata
    """
    return render(request, "./404.html", {})


def homepage(request):
    return render(request, "./index.html")


def presentation(request):
    return render(request, "./presentation.html")


def download_ppt(request):
    try:
        file_path = "./static/img/Lista1.pptx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as ppt_file:
                response = HttpResponse(
                    ppt_file.read(),
                    content_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
                response["Content-Disposition"] = "attachment; filename='Lista1.pptx'"
                return response
        else:
            return HttpResponse("File non trovato.", status=404)
    except Exception as e:
        Log().logMe(e)
        return HttpResponse("Impossibile recuperare il file in questo momento")


def desktop(request):
    context = {
        "chcontent" : content_changelog(),
    }
    return render(request, "./desktop.html", context)


@csrf_exempt
def chatbot_ask(request):
    """
    *   Funzione che si attiva quando si fa una richiesta di tipo GET
    *   al percorso /chatbot/ask/.
    *   Questa funzione restituisce un json con la risposta del chatbot
    """
    try:
        if request.method == "POST":
            question = request.POST.get('question')

            m = Model(os.getenv("GROQ_API_KEY"), language="italian")
            response = asyncio.run(m.chat(question))

            try:
                LogBot(question, response).logMe()
            except Exception as e:
                print(e)

            return JsonResponse({"response": response})
        else:
            return JsonResponse({"error": "Invalid request method"}, status=400)
    except Exception as e:
        print(e)
        Log().logMe(e)
        return JsonResponse({"error": "Invalid request method"}, status=400)


def forum(request):
    """
    *   Prendo tutte le domande dalla tabella MemoryDomande del db 
    *   e lo mostro nella pagina del forum.
    *   Il contenuto di ogni domanda (SOLO nella homepage del forum) viene
    *   mostrata una parte, questo perchè ci possono essere domande molto
    *   lunghe che potrebbero occupare un sacco di spazio della pagina web.
    *   Quindi ho deciso che verranno mostrati solo i primi 20 char del contenuto
    *
    *   N.B: viene fatto un controllo delle domande sul contenuto anche in questa fase, perchè
    *   se per sbaglio qualcuno riesce ipoteticamente ad accedere alla suite admin,
    *   e a modificare il contenuto dei db, potrebbe riuscire a scrivere schifezza. 
    *   Quindi in caso succeda, ho deciso di fare un controllo aggiuntivo.
    """
    domande_reverse = MemoryDomande.objects.all()[::-1]
    ban_word = set(BanWord.objects.all())

    for domanda in domande_reverse:
        if (paragona(domanda.titolo.upper(), ban_word) == False and 
            paragona(domanda.content.upper(), ban_word) == False):

            if len(domanda.content) > 21:
                domanda.content = domanda.content[0:20]
            else: 
                domanda.content = domanda.content

        else:   # non faccio comparire la domanda
            domanda.titolo = ''
            domanda.content = ''

    paginator = Paginator(domande_reverse, 20)  # Mostra 20 domande per pagina
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    for ora in page_obj:
        # uso una regex per aggiustare il formato della data
        ora.datetime = re.sub(r"(\.\d*)", " ", ora.datetime) if ora.datetime != "None" else ora.datetime

    context = {
        "page_obj" : page_obj
    }
    return render(request, "./forum/forum.html", context)


def filter_questions(request):
    """
    *   Funzione che restituisce un json contenente tutte le domande all'interno della tabella MemoryDomande.
    *   Questa funzione si attiva alla richiesta di tipo get al percorso /forum/filter/.
    """
    query = request.GET.get("q", "")
    ban_word = set(BanWord.objects.all())
    questions = MemoryDomande.objects.all()

    context = []
    for question in questions:
        if (paragona(question.titolo.upper(), ban_word) == False and 
            paragona(question.titolo.upper(), ban_word) == False):
            # uso una regex per aggiustare il formato della data
            context.append({
                "id":       question.id,
                "titolo":   question.titolo,
                "content":  question.content,
                "datetime": re.sub(r"(\.\d*)", " ", question.datetime) if question.datetime != "None" else question.datetime 
            })

    return JsonResponse({"questions": context})


def form_forum(request):
    if request.method == "POST":
        ban_word = set(BanWord.objects.all())
        
        form = FormDomanda(request.POST)
        if form.is_valid():
            db_domanda = MemoryDomande()
            db_domanda.titolo = form.cleaned_data["titolo"]
            db_domanda.content = form.cleaned_data["contenuto"]
            db_domanda.username = form.cleaned_data["username"]
            db_domanda.password = form.cleaned_data["password"]
            try:
                # bypasso problemi di sicurezza
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                session = requests.Session()

                # verifico se username e password sono corretti
                response = session.post(
                    "https://campus.marconivr.it/login/index.php", 
                    data = {
                        "username": db_domanda.username, 
                        "password": db_domanda.password
                    },
                    verify = False
                )

                if "Dashboard" in response.text: # se sono corretti
                    if client_request(db_domanda.username) == "troppi tentativi per singola matricola":
                        return render(request, "./forum/error.html", {"causa" : "Errore! hai mandato troppe richieste velocemente! aspetta un pò prima di mandarne altre"})

                    # verifico che non ci siano parole bannabili all'interno db_domanda.titolo e db_domanda.content
                    # e va alla schermata successiva, altrimenti se sono state detectate delle parole bannabili
                    # il form non viene salvato e da un messaggio di errore sulla pagina web
                    
                    ban_word = set(BanWord.objects.values_list("word", flat = True))
                    if paragona(db_domanda.titolo, ban_word) == False and paragona(db_domanda.content, ban_word) == False:                    
                        db_domanda.username, db_domanda.ukey    = Security.generate(db_domanda.username)
                        db_domanda.password, db_domanda.pkey    = Security.generate(db_domanda.password)
                        db_domanda.datetime                     = datetime.now()
                        id_page                                 = len(MemoryDomande.objects.all())
                        db_domanda.content                      = db_domanda.content
                        db_domanda.titolo                       = db_domanda.titolo
                        db_domanda.save()
                        messages.success(request, "La tua domanda è stata pubblicata con successo!")
                        return redirect("forum_domanda", id = id_page + 1)  # Usa redirect per passare all'URL corretto
                    else:
                        messages.error(request, "Errore! Hai usato delle parole non consentite, sei pregato di calmarti e riflettere su quello che stai scrivendo")
                        return render(request, "./forum/error.html", {"causa" : "Errore! Hai usato delle parole non consentite, sei pregato di calmarti e riflettere su quello che stai scrivendo"})    

                elif "manteniance mode" in response.text: # caso in cui il server di campus è in manutenzione
                    messages.error(request, "Errore! impossibile validare username e password causa: campus in manutenzione")
                    return render(request, "./forum/error.html", {"causa": "Errore! impossibile validare username e password causa: campus in manutenzione"})

                else:
                    messages.error(request, "Password o username invalidi!")
                    return render(request, "./forum/error.html", {"causa" : "Password o username invalidi!"})
            except RequestException as e:
                # Gestione degli errori di rete
                messages.error(request, "Errore di connessione al sito esterno. Riprova più tardi.")
                Log().logMe(f"Errore di rete: {str(e)}")
                return render(request, "./forum/error.html", {"causa": f"Errore di rete: {str(e)}"})
    else:
        form = FormDomanda()

    context = {"form" : form}
    return render(request, "./forum/form.html", context)


def forum_domanda(request, id):
    """*
    *   Funzione che viene attivata quando si accede alla domanda
    *   del forum.   
    *"""
    if int(id) >= 0 and int(id) <= len(MemoryDomande.objects.all()):
        ban_word = set(BanWord.objects.all())
        if request.method == "POST": 
            form_answer = FormRisposta(request.POST)

            if form_answer.is_valid():
                answ = MemoryRisposte()
                answ.token_id = int(id)
                answ.content = form_answer.cleaned_data["contenuto"]
                answ.username = form_answer.cleaned_data["username"]
                answ.password = form_answer.cleaned_data["password"]

                # verifico se username e password sono corretti
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                session = requests.Session()

                # verifico se username e password sono corretti
                response = session.post(
                    "https://campus.marconivr.it/login/index.php", 
                    data = {
                        "username": answ.username, 
                        "password": answ.password
                    },
                    verify = False
                )

                if "Dashboard" in response.text:
 
                    if client_request(answ.username) == "troppi tentativi per singola matricola":
                        return render(request, "./forum/error.html", {"causa" : "Errore! hai mandato troppe richieste velocemente! aspetta un pò prima di mandarne altre"})

                    ban_word = set(BanWord.objects.values_list("word", flat=True))
                    if paragona(answ.content.upper(), ban_word) == False:
                        answ.username, answ.ukey = Security.generate(answ.username)
                        answ.password, answ.pkey = Security.generate(answ.password)
                        answ.save()
                        messages.success(request, "La tua risposta è stata pubblicata con successo!")
                        return redirect("forum_domanda", id = id)
                    else:
                        messages.error(request, "Errore! Hai usato delle parole non consentite, sei pregato di calmarti e riflettere su quello che stai scrivendo")
                        return render(request, "./forum/error.html", {"causa" : "Errore! Hai usato delle parole non consentite, sei pregato di calmarti e riflettere su quello che stai scrivendo"})
                
                elif "manteniance mode" in response.text: # caso in cui il server di campus è in manutenzione
                    messages.error(request, "Errore! impossibile validare username e password causa: campus in manutenzione")
                    return render(request, "./forum/error.html", {"causa": "Errore! impossibile validare username e password causa: campus in manutenzione"})

                else:
                    messages.error(request, "Password o username invalidi!")
                    return render(request, "./forum/error.html", {"causa" : "Password o username invalidi!"})

        else:
            form_answer = FormRisposta()
            single_case = MemoryDomande.objects.get(id = id)

            try:
                # prendo tutte le risposte a una singola domanda (dalla più recente alla più vecchia)
                answer_single_case = MemoryRisposte.objects.filter(token_id = id)[::-1] 

                context = {
                    "caso"          : single_case,
                    "form_answer"   : form_answer,  
                    "answer"        : answer_single_case
                }

            except MemoryRisposte.DoesNotExist: # caso in cui non esistono risposte per quella domanda
                context = {
                    "caso"          : single_case,
                    "form_answer"   : form_answer
                }

            return render(request, "forum/question/case.html", context)
    else:
        return render(request, "./404.html", {})


def library(request):
    """*
    *   Viene usato il try nel caso in cui da sito di tiobe dovessero modificare i nomi delle intestazioni
    *   tiobe_header.remove("Change") -> se manca "Change" da errore!
    *"""
    try:
        link_table = "https://www.tiobe.com/tiobe-index/"
        tiobe_header, tiobe_content = web_scraping(link_table, "table table-striped table-top20")

        if tiobe_header == None or tiobe_content == None:           # caso in cui qualcosa è andato storto mentre cercavo di ottenere dati
            Log().logMe(f"errore durante l'estrazione dei dati dalla tabella di tiobe: variabile tiobe_header o tiobe_content == None!")
            return render(request, "./library/library.html", {})    # non mostro la table di tiobe

        else:
            tiobe_header.remove("Change")

        lista = []
        for line in tiobe_content:                                          # Creo una lista bidimesionale che contiene tiobe_content pulito
            rank_current    = re.match(r"^\d+", line).group()               # Regex per trovare il primo numero (classifica attuale)
            line            = re.sub(r"^\d+\s+", "", line)                  # Rimuove il primo numero dalla stringa
            rank_previous   = re.match(r"^\d+", line).group()               # Regex per trovare il secondo numero (classifica precedente)
            line            = re.sub(r"^\d+\s+", "", line)                  # Rimuove il secondo numero dalla stringa
            rating_change   = re.search(r"[\+\-]\d+\.\d+%", line).group()   # Regex per trovare l'ultima percentuale (cambio di rating)
            line            = re.sub(r"[\+\-]\d+\.\d+%$", "", line).strip() # Rimuove l'ultima percentuale dalla stringa

            # Splitta il resto della stringa tra nome del linguaggio e rating attuale
            parts           = line.rsplit(" ", 1)
            language        = parts[0]
            rating_current  = parts[1]
            lista.append([rank_current, rank_previous, language, rating_current, rating_change])

        context = {
            "head" : tiobe_header,
            "body" : lista,
            "tiobe" : link_table,
        }
        return render(request, "./library/library.html", context)
    except Exception as e:
        Log().logMe(f"errore durante l'estrazione dei dati dalla tabella di tiobe: {e}")
        return render(request, "./library/library.html", {})


"""
*   Per migliorare la leggibilità raggruppo le lezioni di ogni sezione in classi
"""
class Nasm_section:
    def intro(request):
        return render(request, './library/assembly/intro.html')

    def lesson(request, num_lesson: str):
        if int(num_lesson) > 0 and int(num_lesson) < 11:  
            return render(request, f'./library/assembly/lezioni/lezione{num_lesson}.html')
        else:
            return render(request, "./404.html", {})


class C_section:
    def intro(request):
        return render(request, './library/c/intro.html')

    def lesson(request, num_lesson: str):
        if int(num_lesson) > 0 and int(num_lesson) < 20:  
            return render(request, f'./library/c/lezioni/lezione{num_lesson}.html')
        else:
            return render(request, "./404.html", {})

    # descrizione standard library
    def stdio(request):
        return render(request, './library/c/lezioni/clibrary/stdio.html')

    def stdlib(request):
        return render(request, './library/c/lezioni/clibrary/stdlib.html')

    def stdint(request):
        return render(request, './library/c/lezioni/clibrary/stdint.html')
    
    def string(request):
        return render(request, './library/c/lezioni/clibrary/string.html')

    def time(request):
        return render(request, './library/c/lezioni/clibrary/time.html')

    def locale(request):
        return render(request, './library/c/lezioni/clibrary/locale.html')
    
    def unistd(request):
        return render(request, './library/c/lezioni/clibrary/unistd.html')
    
    def errno(request):
        return render(request, './library/c/lezioni/clibrary/errno.html')

    def stdarg(request):
        return render(request, './library/c/lezioni/clibrary/stdarg.html')

    def stdbool(request):
        return render(request, './library/c/lezioni/clibrary/stdbool.html')

    def stddef(request):
        return render(request, './library/c/lezioni/clibrary/stddef.html')

    def search(request):
        return render(request, './library/c/lezioni/clibrary/search.html')

    def types(request):
        return render(request, './library/c/lezioni/clibrary/types.html') 

    def ctype(request):
        return render(request, './library/c/lezioni/clibrary/ctype.html') 

    def signal(request):
        return render(request, './library/c/lezioni/clibrary/signal.html') 


class Cpp_section:
    def intro(request):
        return render(request, './library/cpp/intro.html')
    
    def lesson(request, num_lesson: str):
        if int(num_lesson) > 0 and int(num_lesson) < 5:  
            return render(request, f'./library/cpp/lezione/lezione{num_lesson}.html')
        else:
            return render(request, "./404.html", {})


class Js_section:
    def intro(request):
        return render(request, 'library/javascript/intro.html')


class Py_section:
    def intro(request):
        return render(request, 'library/python/intro.html')
    
    def lesson(request, num_lesson: str):
        if int(num_lesson) > 0 and int(num_lesson) < 8:  
            return render(request, f'./library/python/lezioni/lezione{num_lesson}.html')
        else:
            return render(request, "./404.html", {})

    # librerie python
    def os(request):
        return render(request,'library/python/lezioni/pylib/os.html')

    def datetime(request):
        return render(request,'library/python/lezioni/pylib/datetime.html')

    def random(request):
        return render(request,'library/python/lezioni/pylib/random.html')

    '''
    def math(request):
        return render(request,'library/python/lezioni/pylib/math.html')

    def re(request):
        return render(request,'library/python/lezioni/pylib/re.html')

    def sys(request):
        return render(request,'library/python/lezioni/pylib/sys.html')

    def json(request):
        return render(request,'library/python/lezioni/pylib/json.html')

    def csv(request):
        return render(request,'library/python/lezioni/pylib/csv.html')

    def urllib(request):
        return render(request,'library/python/lezioni/pylib/urllib.html')
    '''
