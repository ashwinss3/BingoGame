from datetime import datetime

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Game(BaseModel):
    class Meta:
        db_table = 'game'

    SIZE_CHOICES = [(3, 3),
                    (4, 4),
                    (5, 5)]
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    end_time = models.DateTimeField()
    size = models.PositiveSmallIntegerField(default=5, choices=SIZE_CHOICES)

    @property
    def is_active(self):
        """Determine is game is active or not"""
        return bool(self.end_time and datetime.now() > self.end_time)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('game-detail', args=[str(self.id)])



class GameOptions(BaseModel):
    class Meta:
        db_table = 'game_options'

    id = models.AutoField(primary_key=True)
    name = models.TextField()
    is_done = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)

    def __str__(self):
        return self.name



class League(BaseModel):
    class Meta:
        db_table = 'league'

    id = models.AutoField(primary_key=True)
    name = models.TextField()
    games = models.ManyToManyField(Game)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('league-detail', args=[str(self.id)])


class UserGame(BaseModel):
    class Meta:
        db_table = 'user_game'
        constraints = [
            models.UniqueConstraint(fields=['user', 'game'], name='one user_game per user')
        ]


    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.PositiveSmallIntegerField(default=0)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('user-game-detail', args=[str(self.id)])



class UserGameChoices(BaseModel):
    class Meta:
        db_table = 'user_game_choices'
        constraints = [
            models.UniqueConstraint(fields=['choice', 'user_game'], name='unique choices')
        ]

    id = models.AutoField(primary_key=True)
    user_game = models.ForeignKey(UserGame, on_delete=models.PROTECT)
    position = models.PositiveSmallIntegerField(default=0)
    choice = models.ForeignKey(GameOptions, on_delete=models.PROTECT)


class LeagueStandings(BaseModel):
    class Meta:
        db_table = 'league_standings'

    id = models.AutoField(primary_key=True)
    league = models.OneToOneField(League, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.PositiveSmallIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    prev_position = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('league-standings', args=[str(self.id)])

