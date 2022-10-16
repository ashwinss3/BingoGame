from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Game, Options, League, UserGame, UserChoices

admin.site.register(User, UserAdmin)
admin.site.register(Game)
admin.site.register(Options)
admin.site.register(League)
admin.site.register(UserGame)
admin.site.register(UserChoices)
