# chat/views.py
from django.shortcuts import render

def index(request):
    print(request)
    return render(request, 'index.html')

def room(request, room_name):
    print(request,room_name)
    return render(request, 'room.html', {
        'room_name': room_name
    })
