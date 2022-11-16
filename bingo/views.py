from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from bingo.forms.game import GameForm, UserGameChoicesForm
from bingo.forms.registration import UserSignupForm
from bingo.models import Game, LeagueStandings, League, UserGame, UserGameChoices, GameOptions
from bingo.utils import utils

from django.views.generic.edit import CreateView


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/signup.html'
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


class LeagueListView(LoginRequiredMixin, generic.ListView):
    model = League
    template_name = 'league/league_list.html'
    paginate_by = 10
    ordering = ['-created_at']


class LeagueStandingView(generic.ListView):
    model = LeagueStandings
    template_name = 'league/league_standings.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return LeagueStandings.objects.filter(league_id=self.kwargs['league_id'])


class UserGameListView(LoginRequiredMixin, generic.ListView):
    model = UserGame
    template_name = 'game/user_game_list.html'
    paginate_by = 10

    def get_queryset(self):
        return UserGame.objects.filter(user=self.request.user).order_by('-created_at')


class UserGameDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserGame
    template_name = 'game/user_game_detail.html'

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

@login_required
def manage_user_game(request, game_id):
    user_game, created = UserGame.objects.get_or_create(user=request.user, game_id=game_id)
    game_size = user_game.game.size * user_game.game.size
    user_game_choice, c_created = UserGameChoices.objects.get_or_create(user_game=user_game)

    saved = False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        user_game_form = UserGameChoicesForm(request.POST, instance=user_game_choice, game_id=user_game.game_id, game_size=game_size)

        # check whether it's valid:
        if user_game_form.is_valid():
            # print(user_game_form.data)
            user_game_form.save(commit=True)
            saved = True
            # uncomment below to redirect to any other page. (redirect to user game detail maybe ?)
            # return HttpResponseRedirect('/thanks/')

    else:
        user_game_form = UserGameChoicesForm(instance=user_game_choice, game_id=user_game.game_id, game_size=game_size)

    game_options = GameOptions.objects.filter(game=user_game.game)

    context = {
        'form': user_game_form,
        'game_size': user_game.game.size,
        'saved': saved,
        'game_options': game_options,
        'game_name': user_game.game.name,
        'is_active': user_game.game.is_active
    }

    return render(request, 'user_game/user_game_create.html', context)


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



