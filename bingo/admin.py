from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Game, GameOptions, League, UserGame, UserGameChoices, LeagueStandings

admin.site.register(User, UserAdmin)
admin.site.register(Game)
admin.site.register(GameOptions)
admin.site.register(League)
admin.site.register(LeagueStandings)
admin.site.register(UserGame)
admin.site.register(UserGameChoices)
