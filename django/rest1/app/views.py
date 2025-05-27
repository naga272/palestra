from django.shortcuts import render
from django.http import JsonResponse  # importa questa


# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie


@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    return Response({"message" : username + " " + password})


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"message": "CSRF token set"})
