from datetime import datetime, timezone


def get_active_games():
    from bingo.models import Game
    return Game.objects.filter(end_time__gt=datetime.now(timezone.utc))


def get_user_choices_list(user_choices, game_size):
    choices_array = []
    for index in range(1, (game_size*game_size)+1):
        choice = getattr(user_choices, f'pos{index}')
        choices_array.append(choice)

    return choices_array

