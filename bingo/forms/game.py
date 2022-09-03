from django import forms
from bingo.models import Game


class GameForm(forms.ModelForm):
    # name = forms.CharField(max_length=128, help_text="Please enter the game name.")
    # end_time = forms.DateTimeField(help_text="Please enter the game end time.")
    # size = forms.IntegerField(widget=forms.Select(choices=Game.SIZE_CHOICES),
    #                           initial=5,
    #                           help_text="Please enter size.")

    class Meta:
        model = Game
        fields = ('name', 'end_time', 'size')
        widgets = {
            'name': forms.TextInput(),
            'end_time': forms.TextInput(attrs={'type': 'datetime'})
        }


