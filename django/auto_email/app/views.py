from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.


def home(request):
    send_mail(
        'Oggetto dell\'email',
        'Corpo del messaggio',
        'bastianellofederico4@gmail.com',
        ['bastianellofederico4@gmail.com'],
        fail_silently=False,
    )
    return render(request, "index.html", {})
