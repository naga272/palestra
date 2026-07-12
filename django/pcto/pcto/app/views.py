from django.shortcuts import render, redirect
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from .models import (
    Filiale, Azienda, Progetto,
    SupervisoreAzienda, Proff, Studente,
    Diario, PaginaDiario, StoricoProgettoStudente
)

from .forms import NewProgetto, NewPagina
from datetime import datetime
import time


def homepage(request: HttpRequest):
    return render(request, "index.html", {})


def page_not_found(request: HttpRequest):
    return render(request, "error404.html")


@login_required
def add_progetto(request: HttpRequest):
    user = request.user

    # verifico che sia effettivamente un account supervisore
    # se non lo e' mostro la pagina 404
    if not hasattr(user, "SupervisoreAzienda"):
        return render(request, "error404.html", {})

    supervisore = user.SupervisoreAzienda

    if request.method == "GET":
        form = NewProgetto()
        return render(request, "new_project.html", {
            "supervisore": supervisore,
            "form": form
        })

    if request.method == "POST":
        form = NewProgetto(request.POST)

        if form.is_valid():

            Progetto.objects.create(
                supervisore=supervisore,
                azienda=supervisore.azienda,
                filiale=supervisore.filiale,
                titolo=form.cleaned_data["titolo"],
                descrizione=form.cleaned_data["descrizione"],
                requisiti=form.cleaned_data["requisiti"],
                tempo_stimato=form.cleaned_data["tempo_stimato"]
            ).save()

            form = NewProgetto()
            return redirect("profile")


def prendi_project_incarico(studente: Studente, progetto: Progetto) -> int:
    if progetto.n_posti_disp == 0:
        return -1

    progetto.n_posti_disp -= 1
    progetto.save()

    studente.progetto = progetto
    studente.filiale = progetto.supervisore.filiale
    studente.timestamp_presa_incarico_p = time.time()
    studente.save()
    return 1


@login_required
def more_info_project(request: HttpRequest, id_progetto: int):
    user = request.user

    if hasattr(user, "studente"):
        studente = user.studente

        if studente.progetto:
            # gli studenti che hanno in incarico un progetto non possono
            # vedere nessuno degli altri progetti
            return render(request, "error404.html", {})

        progetto = Progetto.objects.get(id=id_progetto)

        if request.method == "POST":
            if prendi_project_incarico(studente, progetto):
                return redirect("profile")

            # caso che e' andato storto
            return render(request, "error_assignement_p.html", {
                    "causa_errore": (
                        "Ci dispiace ma il progetto ha"
                        "raggiunto il limite di studenti assegnati!"
                        )
                })

        info = {
            "type_account": "studente",
            "studente":     studente,
            "progetto":     progetto,
            "data_creazione": datetime.fromtimestamp(
                progetto.timestamp_creazione
            ),
            "diario":       Diario.objects.get(studente_id=studente.id)
        }

    elif hasattr(user, "SupervisoreAzienda"):
        # supervisore vuole vedere le info del progetto e
        # vuole vedere quali studenti sono assegnati al progetto
        supervisore = user.SupervisoreAzienda
        progetto = Progetto.objects.get(id=id_progetto)

        if progetto.supervisore != supervisore:
            # solo il supervisore che ha creato il progetto
            # puo' visualizzare le informazioni del suo progetto
            return redirect(request, "page_not_found")

        all_students_assigned = Studente.objects.filter(
            progetto__id=id_progetto
        )

        students_and_diaries = [
            {
                "studente": studente,
                "diario": Diario.objects.get(studente=studente)
            }
            for studente in all_students_assigned
        ]

        info = {
            "type_account": "supervisore",
            "progetto": progetto,
            "students_and_diaries": students_and_diaries,
            "data_creazione": datetime.fromtimestamp(
                progetto.timestamp_creazione
            )
        }

    else:
        # caso in cui non e' loggato o non e' studente o supervisore
        return redirect("page_not_found")

    return render(request, "dettagli_progetto.html", info)


@login_required
def display_diario(request: HttpRequest, diario_id: int):
    user = request.user

    if not hasattr(user, "SupervisoreAzienda"):
        return redirect("page_not_found")

    supervisore = user.SupervisoreAzienda
    diario = Diario.objects.get(id=diario_id)
    print("form valido")
    if request.method == "POST":
        form = NewPagina(request.POST)
        if form.is_valid():
            print("form valido")
            PaginaDiario.objects.create(
                diario=diario,
                supervisore=supervisore,
                contenuto=form.cleaned_data["contenuto"],
            )
        else:
            print("error")

        return redirect("display_diario", diario_id=diario_id)

    pagine = PaginaDiario.objects.filter(diario=diario)

    info = {
        "studente": diario.studente,
        "pagine": pagine,
        "formNewPagina": NewPagina()
    }

    return render(request, "display_diario.html", info)


def elab_res_x_profile_stud(request: HttpRequest, studente: Studente) -> dict:
    """
    IL PRIMO CHE INCLUDE IN URLS.PY QUESTA FUNZIONE LO DENUNCIO ALLA POLIZIA
    elabora la configurazione di un dizionario contenente informazioni
    relative allo studente che ha chiesto la pagina

    Args:
        request (HttpRequest): informazioni generali relative al client
                                (method, ...)
        studente (Studente): studente che ha richiesto la pagina

    Returns:
        dict: contiene le informazioni dello studente
                pronte da passare alla foo render()
    """
    info = {}
    if request.method == "POST":
        # significa che ha fatto la richiesta
        # per abbandonare il progetto
        progetto = studente.progetto
        StoricoProgettoStudente.objects.create(
            studente=studente,
            progetto=progetto,
            timestamp_abbandono=time.time()
        ).save()

        # libero un posto dal progetto
        progetto.n_posti_disp += 1
        progetto.save()

        studente.progetto = None
        studente.presa_in_incarico_p = 0.0
        studente.save()

    if not studente.progetto:
        # se lo studente non ha gia' preso
        # in incarico un progetto mostro
        # l'elenco di progetti (esclusi quelli
        # abbandonati dallo studente)
        progetti_abbandonati = StoricoProgettoStudente.objects.filter(
            studente=studente
        ).values_list("progetto_id", flat=True)

        info["elenco_progetti"] = Progetto.objects.filter(
            is_completato=False
        ).exclude(
            id__in=progetti_abbandonati
        ).exclude(n_posti_disp=0)

    else:
        info["progetto_in_carica"] = studente.progetto
        info["supervisore"] = info["progetto_in_carica"].supervisore
        info["filiale_assegnata"] = info["supervisore"].filiale
        info["azienda"] = info["filiale_assegnata"].azienda

    diario = Diario.objects.get(studente=studente)
    info["pagine"] = PaginaDiario.objects.filter(diario=diario)
    info["studente"] = studente
    info["type_profilo"] = "studente"
    return info


@login_required
def profile(request: HttpRequest):
    user = request.user
    info = {"user": user}

    if hasattr(user, "SupervisoreAzienda"):
        supv = user.SupervisoreAzienda
        info.update({
            "type_profilo": "azienda",
            "supervisore":  supv,
            "azienda":      supv.filiale.azienda,
            "progetti":     Progetto.objects.filter(
                supervisore__filiale=supv.filiale
            )
        })

    elif hasattr(user, "studente"):
        info.update(elab_res_x_profile_stud(request, user.studente))

    elif hasattr(user, "proff"):
        info.update({
            "type_profilo": "proff",
            "anagrafica":   user.proff,
            "diari":        Diario.objects.all(),
            "studenti":     Studente.objects.all()
        })

    else:
        return redirect("login")

    return render(request, "profilo.html", info)


def constactUs(request: HttpRequest):
    if request.method == "GET":
        return render(request, "contactUs.html", {})
