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


def validate_game_end(game_id, deny_active=False, deny_inactive=False):
    from bingo.models import Game
    game_obj = Game.objects.get(id=game_id)
    is_game_active = game_obj.is_active
    if is_game_active and deny_active:
        raise PermissionError('Wait till game deadline :)')
    if not is_game_active and deny_inactive:
        raise PermissionError('Game deadline finished :)')

    return game_obj
