
from django.urls import path
from bingo import views

urlpatterns = [
    path('', views.index, name="index"),
    path('game/', views.game, name="game"),
]
