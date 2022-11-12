from django import forms
from django.forms import BaseInlineFormSet

from bingo import config
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
        fields = '__all__'
        exclude = ('user_game', 'deleted_at')

    def __init__(self, *args, **kwargs):
        self.game_id = kwargs.pop('game_id')
        self.game_size = kwargs.pop('game_size', 25)
        super().__init__(*args, **kwargs)
        extra_positions = config.MAX_GAME_SIZE - self.game_size
        # deleting any extra fields. Since we have 25 fields by default
        for i in range(extra_positions):
            self.fields.pop(f'pos{config.MAX_GAME_SIZE-i}')
        game_choices = GameOptions.objects.filter(game_id=self.game_id)
        for num in range(1, self.game_size+1):
            # updating queryset for all position
            self.fields[f'pos{num}'].queryset = game_choices
            self.fields[f'pos{num}'].widget.attrs['class'] = 'bingo-card__item'

class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'end_time', 'size')
        widgets = {
            'name': forms.TextInput(),
            'end_time': forms.TextInput(attrs={'type': 'datetime'})
        }


