
from django.urls import path
from bingo import views

urlpatterns = [
    path('', views.index, name="index"),
    path('game/', views.game, name="game"),
    path('games/', views.GameListView.as_view(), name='games'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    path('leagues/', views.LeagueListView.as_view(), name='leagues'),
    path('league-standing/<int:league_id>', views.LeagueStandinglView.as_view(), name='league-standings'),
    path('my-games/', views.UserGameListView.as_view(), name='user-games'),
    path('my-game/<int:pk>', views.UserGameDetailView.as_view(), name='user-game-detail'),
    path('my-game/<int:game_id>/create/', views.manage_user_game, name='user-game-create'),

]
