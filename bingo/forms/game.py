from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from bingo import config
from bingo.models import Game, UserGameChoices, GameOptions


class UserGameChoicesForm(forms.ModelForm):

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

    def clean(self):
        game = Game.objects.get(id=self.game_id)
        if not game.is_active:
            raise ValidationError('Game Deadline Crossed')
        super().clean()
        field_counts = {}
        for num in range(1, self.game_size + 1):
            option = self.cleaned_data[f'pos{num}']
            field_counts[option] = field_counts.get(option, 0) + 1

        # filtering out to keep only ones with count > 1
        field_counts = {key: value for key, value in field_counts.items() if value > 1}

        if field_counts:
            for field, value in self.cleaned_data.items():
                if value in field_counts:
                    self.fields[field].widget.attrs['class'] = 'bingo-card__item__error'

            raise ValidationError("Same option selected for more than one field")


class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'end_time', 'size')
        widgets = {
            'name': forms.TextInput(),
            'end_time': forms.TextInput(attrs={'type': 'datetime'})
        }


