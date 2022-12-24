from django.db.models import Subquery, OuterRef, F

from bingo.models import UserGameChoices, UserGame, LeagueStandings
from bingo.utils.utils import validate_game_end

BINGO_LINE_SCORE = 10


def calculate_user_game_score(game_id, game_size):
    validate_game_end(game_id, deny_active=True)

    # {user_game_id: [user_choices.is_done]}
    user_choice = get_user_choice_map(game_id, game_size)

    # {user_game_id: sore}
    user_game_score = get_user_score(user_choice, game_size)

    update_user_game_score_in_db(game_id, user_game_score)


def get_user_choice_map(game_id, game_size):
    # getting choices of each usergame
    position_fields = [f'pos{index}__is_done' for index in range(1, (game_size*game_size)+1)]
    user_choices = UserGameChoices.objects.filter(user_game__game_id=game_id).values('user_game_id', *position_fields)
    choice_array = {}
    for choice in user_choices:
        ug_id = choice.pop('user_game_id')
        choice_array[ug_id] = list(choice.values())

    return choice_array


def get_user_score(user_choice, game_size):
    def get_horizontal_count(user_choice_array):
        horizontal_bingo_count = 0
        for i in range(game_size):
            if all(user_choice_array[game_size*i: game_size*(i+1)]):
                horizontal_bingo_count += 1
        return horizontal_bingo_count

    def get_vertical_count(user_choice_array):
        vertical_bingo_count = 0
        for i in range(game_size):
            """
            logic checks for
            [0, 3, 6]
            [1, 4, 7]
            [2, 5, 8]
            combinations in a 3 game_size array
            """
            if all([user_choice_array[i+(game_size*j)] for j in range(game_size)]):
                vertical_bingo_count += 1
        return vertical_bingo_count

    def get_diagonal_count(user_choice_array):
        """
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]

        left diagonal will always 0, (game_size+1), (game_size+1)*2 , (game_size+1)*3...
        right diagonal will always (game_size-1), (game_size-1)*2 , (game_size-1)*3...
        """
        if game_size % 2 == 0:
            # even number size will not have diagonals
            return 0

        diagonal_bingo_count = 0
        left_diagonal = [user_choice_array[(game_size+1)*i] for i in range(game_size)]
        right_diagonal = [user_choice_array[(game_size-1)*i] for i in range(1, game_size+1)]
        if all(left_diagonal):
            diagonal_bingo_count += 1
        if all(right_diagonal):
            diagonal_bingo_count += 1

        return diagonal_bingo_count

    user_game_score = {}
    for user_game_id, choice_array in user_choice.items():
        bingo_count = 0
        bingo_count += get_horizontal_count(choice_array)
        bingo_count += get_vertical_count(choice_array)
        bingo_count += get_diagonal_count(choice_array)
        user_game_score[user_game_id] = bingo_count * BINGO_LINE_SCORE

    return user_game_score


def update_user_game_score_in_db(game_id, user_game_scores):
    user_games = UserGame.objects.filter(game_id=game_id)
    for user_game in user_games:
        user_game.score = user_game_scores.get(user_game.id) or 0

    UserGame.objects.bulk_update(user_games, ['score'])


def update_league_standing_for_user_game(game_id, league_id):
    """
    Function to update the score in league standings
    """
    score_subquery = Subquery(
        UserGame.objects.filter(user_id=OuterRef('user_id'), game_id=game_id).values('score')
    )
    LeagueStandings.objects.filter(league_id=league_id).update(score=F('score') + score_subquery)


def update_league_standing_positions(league_id, update_prev_position=True):
    # updating positions based on latest score in League Standings
    ordered_standings = LeagueStandings.objects.filter(league_id=league_id).order_by('-score')

    current_position = 1
    prev_score = 0
    for index, standing in enumerate(ordered_standings):
        if update_prev_position:
            # updating the prev_position field only if flag is passed
            standing.prev_position = standing.position

        if standing.score == prev_score:
            standing.position = current_position
        else:
            standing.position = index + 1
            current_position = index + 1
            prev_score = standing.score

    updated_fields = ['position', 'prev_position'] if update_prev_position else ['position']

    LeagueStandings.objects.bulk_update(ordered_standings, updated_fields)
