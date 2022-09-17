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
    deleted_at = models.DateTimeField(null=True)


class Game(BaseModel):
    SIZE_CHOICES = [(3, 3),
                    (4, 4),
                    (5, 5)]
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    end_time = models.DateTimeField()
    size = models.PositiveSmallIntegerField(default=5, choices=SIZE_CHOICES)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('game-detail', args=[str(self.id)])



class Options(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    is_done = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)


class League(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    games = models.ManyToManyField(Game)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('league-detail', args=[str(self.id)])



class UserGame(BaseModel):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.PositiveSmallIntegerField(default=0)


class UserChoices(BaseModel):
    class Meta:
        db_table = 'bingo_user_choices'
        constraints = [
            models.UniqueConstraint(fields=['choice', 'user_game'], name='unique choices')
        ]

    id = models.AutoField(primary_key=True)
    user_game = models.ForeignKey(UserGame, on_delete=models.PROTECT)
    position = models.PositiveSmallIntegerField(default=0)
    choice = models.ForeignKey(Options, on_delete=models.PROTECT)


class LeagueStandings(BaseModel):
    id = models.AutoField(primary_key=True)
    league = models.OneToOneField(League, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.PositiveSmallIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    prev_position = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('league-standings', args=[str(self.id)])

