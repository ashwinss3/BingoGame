from django.shortcuts import render
from bingo.forms.game import GameForm
from django.http import HttpResponseRedirect
from bingo.models import Game, LeagueStandings, League, UserGame
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic


class GameListView(generic.ListView):
    model = Game
    template_name = 'game/game_list.html'
    paginate_by = 10


class GameDetailView(generic.DetailView):
    model = Game
    template_name = 'game/game_detail.html'


class LeagueListView(LoginRequiredMixin, generic.ListView):
    model = League
    template_name = 'league/league_list.html'
    paginate_by = 10


class LeagueStandinglView(generic.ListView):
    model = LeagueStandings
    template_name = 'league/league_standings.html'
    paginate_by = 10

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


def index(request):
    """View function for home page of site."""

    # Generate counts of some main objects

    context = {
        'num_games': 10,
        'num_leagues': 5,
        'num_users': 3,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

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



