from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators    import api_view
from django.http                   import JsonResponse
from .models                      import User


@api_view(["POST"])
def get_registrazione(request):
    User.objects.create(
        username    = request.data.get("username"),
        nome        = request.data.get("nome"),
        cognome     = request.data.get("cognome"),
        password    = request.data.get("password"),
        eta         = request.data.get("eta"),
    )
    return JsonResponse({"answer" : "registrato con successo"}) 


@ensure_csrf_cookie
def get_token(request):
    return JsonResponse({"" : ""})
