from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from app.forms import Tracking
from app.models import Consegna


def tracking(request):
    if request.method != 'GET':
        return JsonResponse({"errore": "richiesta non valida"})

    form = Tracking(request.GET)

    if not form.is_valid():
        return JsonResponse({"errore": "dati non validi"})

    chiave = form.cleaned_data["chiaveConsegna"]

    try:
        consegna = Consegna.objects.get(chiaveConsegna=chiave)
    except Consegna.DoesNotExist:
        return JsonResponse({"errore": "non trovata"})

    return JsonResponse({
        "id_consegna": consegna.chiaveConsegna,
        "stato": consegna.stato,
        "dataRitiro": consegna.dataRitiro,
        "dataConsegna": consegna.dataConsegna,
    })


def homepage(request):
    return render(
        request,
        "index.html",
        context={
            "form": Tracking()
        }
    )
