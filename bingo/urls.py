
from django.urls import path
from bingo import views

urlpatterns = [
    # path('test/', bingo_view_test, name="bingo"),
    path('game/', views.game, name="game"),
]
