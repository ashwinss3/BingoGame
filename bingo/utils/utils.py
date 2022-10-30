from datetime import datetime


def get_active_games():
    from bingo.models import Game
    return Game.objects.filter(end_time__gt=datetime.utcnow())
