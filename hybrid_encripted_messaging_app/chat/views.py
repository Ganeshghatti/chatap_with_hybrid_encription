# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "index.html")

def file(request):
    return render(request, "file.html")

def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})
