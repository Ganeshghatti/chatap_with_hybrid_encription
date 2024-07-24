# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("roomID/<str:room_name>/", views.room, name="room"),
    path("file", views.file, name="file"),
]
