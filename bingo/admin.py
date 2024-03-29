from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Game, GameOptions, League, UserGame, UserGameChoices, LeagueStandings

class PerGameOptions(admin.ModelAdmin):
    list_display = ('name', 'is_done')
    list_filter = ('game',)

admin.site.register(User, UserAdmin)
admin.site.register(Game)
admin.site.register(GameOptions, PerGameOptions)
admin.site.register(League)
admin.site.register(LeagueStandings)
admin.site.register(UserGame)
admin.site.register(UserGameChoices)
