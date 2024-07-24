from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('file/', views.file, name='file'),
    path('decrypt/', views.decrypt_file_view, name='decrypt_file'),
    path('room/<str:room_name>/', views.room, name='room'),
]
