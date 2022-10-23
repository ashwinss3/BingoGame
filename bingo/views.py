from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.views import generic
from django.views.generic.edit import CreateView

from bingo.forms.game import GameForm, UserGameBaseFormset
from bingo.models import Game, LeagueStandings, League, UserGame, UserGameChoices

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


class UserGameCreate(CreateView):
    model = UserGame
    fields = '__all__'
    template_name = 'user_game/user_game_create.html'



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

@login_required
def manage_user_game(request, game_id):
    user_game, created = UserGame.objects.get_or_create(user=request.user, game_id=game_id)
    game_size = user_game.game.size * user_game.game.size

    UserFormSet = inlineformset_factory(UserGame, UserGameChoices, fields=['position', 'choice'],
                                        min_num=game_size, max_num=game_size, validate_max=True,
                                        validate_min=True, formset=UserGameBaseFormset, can_delete=False)
    saved = False


    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formset = UserFormSet(request.POST, instance=user_game)

        # check whether it's valid:
        if formset.is_valid():
            print(formset.data)
            formset.save()
            saved = True
            # uncomment below to redirect to any other page. (redirect to user game detail maybe ?)
            # return HttpResponseRedirect('/thanks/')

    else:
        formset = UserFormSet(initial=[{'position': pos+1} for pos in range(game_size)],
                              instance=user_game)

    context = {
        'formset': formset,
        'saved': saved
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



