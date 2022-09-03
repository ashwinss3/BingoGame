from django.shortcuts import render
from bingo.forms.game import GameForm
from django.http import HttpResponseRedirect


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



