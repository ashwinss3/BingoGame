from django import forms
from django.forms import BaseInlineFormSet

from bingo.models import Game, UserGameChoices, GameOptions


class UserGameBaseFormset(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        # todo: add validations here to make sure positions and choices are unique and correct.


class UserGameChoicesForm(forms.ModelForm):
    # todo: Not being used probably. Can be deleted later.

    class Meta:
        model = UserGameChoices
        fields = ('choice', 'position')

    def __init__(self, *args, **kwargs):
        self.game_id = kwargs.pop('game_id')
        self.user_game_id = kwargs.pop('user_game_id')
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = GameOptions.objects.filter(game_id=self.game_id)


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'end_time', 'size')
        widgets = {
            'name': forms.TextInput(),
            'end_time': forms.TextInput(attrs={'type': 'datetime'})
        }


