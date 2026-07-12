from django.http import JsonResponse
# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login as auth_login
from .models import DirectoryUser
import time


@ensure_csrf_cookie
def get_token(request):
    return JsonResponse({"": ""})


n_richieste = []


def client_request(username: str) -> str:
    """
    * Per motivi di sicurezza ogni client può mandare un massimo di 5 richieste al minuto.
    * Questa funzione tramite la lista n_richieste, controlla se la stessa username
    * manda più di 5 richieste al minuto. restituisce valore "va bene" se il client non supera questo limite,
    * altrimenti darà "troppi tentativi per singola username".
    *
    * @username: la username che identifica il singolo studente
    """
    global n_richieste

    max_requests_per_minute = 3
    time_window_seconds = 60
    current_time = time.time()

    # n_richieste rimuove richieste più vecchie di 60 secondi
    n_richieste = [req for req in n_richieste if current_time - req[1] <= time_window_seconds]

    # Contatore di numero richieste dallo stesso client
    counter = sum(1 for req in n_richieste if req[0] == username)

    if counter < max_requests_per_minute:
        n_richieste.append((username, current_time))
        return True
    else:
        return False


def get_directory_tree_structured(directory):
    tree = {
        "type": "directory",
        "id": directory.id,
        "name": directory.nome,
        "children": [],
        "creation_date": directory.creation_date,
        "last_update": directory.last_modify_date
    }

    for file in directory.file.all():
        tree["children"].append({
            "type": "file",
            "id": file.id,
            "name": file.nome,
            "content": file.content,
            "creation_date": file.creation_date,
            "last_update": file.last_modify_date
        })

    for subdir in directory.subdirectories.all():
        tree["children"].append(get_directory_tree_structured(subdir))

    return tree


def get_filesystem_structured(user):
    root_dirs = DirectoryUser.objects.filter(user=user, parent=None)
    return [get_directory_tree_structured(root) for root in root_dirs]


@api_view(["POST"])
def login(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        print(username, password)

        DEBUG = True

        if DEBUG:  # client_request(username):
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                answer = {
                    "success": True,
                    "filesystem": get_filesystem_structured(user)
                }

            else:
                answer = {
                    "success": False,
                    "error": "Credenziali non valide"
                }
        else:
            answer = {
                "success": False,
                "error": "Hai eseguito troppi tentativi! ora aspetta"
            }
        return JsonResponse(answer)
