import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from bingo.forms.game import GameForm, UserGameChoicesForm
from bingo.forms.registration import UserSignupForm
from bingo.models import Game, LeagueStandings, League, UserGame, UserGameChoices, GameOptions, User
from bingo.utils import utils

from django.views.generic.edit import CreateView

from bingo.utils.utils import get_user_choices_list, validate_game_end


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserSignupForm
    success_message = "Your profile was created successfully"


class GameListView(generic.ListView):
    model = Game
    template_name = 'game/game_list.html'
    paginate_by = 10
    ordering = ['-created_at']


class GameDetailView(generic.DetailView):
    model = Game
    template_name = 'game/game_detail.html'


class LeagueListView(generic.ListView):
    model = League
    template_name = 'league/league_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        params = {}
        if self.request.GET.get('is_active') == 'false':
            params['is_active'] = False
        else:
            params['is_active'] = True

        return League.objects.filter(**params)



class LeagueStandingView(generic.ListView):
    model = LeagueStandings
    template_name = 'league/league_standings.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return LeagueStandings.objects.filter(league_id=self.kwargs['league_id']).order_by('-score')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # todo: check this later. Not using the league games field.
        # context['last_game_id'] = League.objects.get(self.kwargs['league_id']).games.\
        #     filter(end_time__lte=timezone.now()).order_by('-end_time').first().id
        context['last_game_id'] = Game.objects.filter(end_time__lte=timezone.now()).order_by('-end_time').first().id
        if self.request.user.is_authenticated:
            context['current_user_standing'] = LeagueStandings.objects.filter(league_id=self.kwargs['league_id'],
                                                                              user=self.request.user).first()

        return context


class UserGameListView(LoginRequiredMixin, generic.ListView):
    model = UserGame
    template_name = 'game/user_game_list.html'
    paginate_by = 10

    def get_queryset(self):
        return UserGame.objects.filter(user=self.request.user).order_by('-created_at')


class UserGameCreate(CreateView):
    model = UserGame
    fields = '__all__'
    template_name = 'user_game/user_game_create.html'


def index(request):
    """View function for home page of site."""

    # Generate counts of some main objects
    active_games = utils.get_active_games()
    context = {
        'active_games': active_games
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def how_to_play(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'how_to_play.html')


@login_required
def manage_user_game(request, game_id):
    try:
        game_obj = validate_game_end(game_id, deny_inactive=True)

        user_game, ug_created = UserGame.objects.get_or_create(user=request.user, game_id=game_id)
        user_game_choice, c_created = UserGameChoices.objects.get_or_create(user_game=user_game)

        saved = False

        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            user_game_form = UserGameChoicesForm(request.POST, instance=user_game_choice, game=game_obj)

            # check whether it's valid:
            if user_game_form.is_valid():
                # print(user_game_form.data)
                user_game_form.save(commit=True)
                saved = True
                # TODO: temporary. Allow users to join the league they want.
                # for league in League.objects.filter(is_active=True):
                #     LeagueStandings.objects.get_or_create(league=league, user=request.user,
                #                                           defaults=dict(user_name=request.user.username))

                # added to handle multiple games running at same time. THis is to join the main league.
                LeagueStandings.objects.get_or_create(league=game_obj.main_league, user=request.user,
                                                      defaults=dict(user_name=request.user.username))

                # uncomment below to redirect to any other page. (redirect to user game detail maybe ?)
                # return HttpResponseRedirect('/thanks/')

        else:
            user_game_form = UserGameChoicesForm(instance=user_game_choice, game=user_game.game)

        game_options = GameOptions.objects.filter(game=user_game.game).exclude(name='FREE SPACE')
        game_option_ids = [option.id for option in game_options]

        context = {
            'form': user_game_form,
            'game_size': user_game.game.size,
            'saved': saved,
            'game_options': game_options,
            'game_option_ids': game_option_ids,
            'game_name': user_game.game.name,
            'is_active': user_game.game.is_active
        }

        return render(request, 'user_game/user_game_create.html', context)
    except Exception as ex:
        traceback.print_exc()
        raise ex


def view_user_game(request, game_id, user_id=None):
    """
    function to view the user game.
    """
    validate_game_end(game_id, deny_active=True)

    if not user_id:
        user_id = request.user.id

    user_name = User.objects.get(id=user_id).username
    user_game = UserGame.objects.get(user_id=user_id, game_id=game_id)
    user_game_choices = user_game.usergamechoices
    game_size = user_game.game.size
    game_name = user_game.game.name
    game_options = GameOptions.objects.filter(game=user_game.game).order_by('-is_done')
    user_choice_list = get_user_choices_list(user_game_choices, game_size)

    context = {
        'user_name': user_name,
        'game_size': game_size,
        'game_name': game_name,
        'score': user_game.score,
        'user_choice_list': user_choice_list,
        'game_options': game_options
    }
    return render(request, 'game/user_game_detail.html', context=context)


def game(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GameForm()

    context = {
        'form': form
    }

    return render(request, 'game/game.html', context)


def test(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'test.html')
