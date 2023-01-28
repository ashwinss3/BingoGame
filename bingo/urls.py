
from django.urls import path
from bingo import views

urlpatterns = [

    path('test/', views.test, name="test"),
    path('', views.index, name="index"),
    path('how-to-play/', views.how_to_play, name="how_to_play"),
    path('game/', views.game, name="game"),
    path('games/', views.GameListView.as_view(), name='games'),
    path('game/<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    path('leagues/', views.LeagueListView.as_view(), name='leagues'),
    path('league-standing/<int:league_id>/', views.LeagueStandingView.as_view(), name='league-standings'),
    path('my-games/', views.UserGameListView.as_view(), name='user-games'),
    path('my-game/<int:game_id>/view/', views.view_user_game, name='user-game-view'),
    path('my-game/<int:game_id>/view/<int:user_id>/', views.view_user_game, name='user-game-view-other'),
    path('user-game/<int:league_id>/view/<int:user_id>/', views.view_user_last_game, name='view-user-last-game'),
    path('my-game/<int:game_id>/manage/', views.manage_user_game, name='user-game-manage'),

    path("signup/", views.SignUpView.as_view(), name="signup"),

]
