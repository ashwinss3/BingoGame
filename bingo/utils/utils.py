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


# [ GAME UTILS ]

def get_user_game_details(user_game):
    user_game_details = {}
    from bingo.models import GameOptions

    user_game_choices = user_game.usergamechoices
    game_size = user_game.game.size
    user_game_details['game_size'] = game_size
    user_game_details['game_name'] = user_game.game.name
    user_game_details['game_options'] = GameOptions.objects.filter(game=user_game.game).order_by('-is_done')
    user_game_details['user_choice_list'] = get_user_choices_list(user_game_choices, game_size)

    return user_game_details


def get_user_game_style_data(game_size):
    # change this function to a class later maybe ?
    # GAME SIZE -> BINGO CARD STYLE DATA MAP
    style_data_map = {
        'default': {
            'grid_gap': '4px',
            'column_gap': '5em',
            'column_max_width': '50em'

    },
        3: {
            'grid_gap': '15px',
            'column_gap': '10em',
            'column_max_width': '30em'
        }
    }
    return style_data_map.get(int(game_size), style_data_map['default'])


