from datetime import datetime, timezone

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
        return bool(self.end_time and datetime.now(timezone.utc) < self.end_time)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('game-detail', args=[str(self.id)])

    def user_game_url(self):
        """Returns URL to set the UserGame associated with current game"""
        if self.is_active:
            return reverse('user-game-manage', args=[str(self.id)])
        else:
            return reverse('user-game-view', args=[str(self.id)])


class GameOptions(BaseModel):
    class Meta:
        db_table = 'game_options'

    id = models.AutoField(primary_key=True)
    name = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    condition = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
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
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('league-detail', args=[str(self.id)])

    def get_standings_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('league-standings', args=[str(self.id)])



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
        if self.game.is_active:
            return reverse('user-game-manage', args=[str(self.game_id)])
        else:
            return reverse('user-game-view', args=[str(self.game_id)])


class UserGameChoices(BaseModel):
    class Meta:
        db_table = 'user_game_choices'

    id = models.AutoField(primary_key=True)
    user_game = models.OneToOneField(UserGame, on_delete=models.PROTECT)
    pos1 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos1', null=True)
    pos2 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos2', null=True)
    pos3 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos3', null=True)
    pos4 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos4', null=True)
    pos5 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos5', null=True)
    pos6 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos6', null=True)
    pos7 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos7', null=True)
    pos8 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos8', null=True)
    pos9 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos9', null=True)
    pos10 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos10', null=True)
    pos11 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos11', null=True)
    pos12 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos12', null=True)
    pos13 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos13', null=True)
    pos14 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos14', null=True)
    pos15 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos15', null=True)
    pos16 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos16', null=True)
    pos17 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos17', null=True)
    pos18 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos18', null=True)
    pos19 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos19', null=True)
    pos20 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos20', null=True)
    pos21 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos21', null=True)
    pos22 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos22', null=True)
    pos23 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos23', null=True)
    pos24 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos24', null=True)
    pos25 = models.ForeignKey(GameOptions, on_delete=models.PROTECT, related_name='pos25', null=True)
    # update config.MAX_GAME_SIZE if the number of positions are being changed


class LeagueStandings(BaseModel):
    class Meta:
        db_table = 'league_standings'
        constraints = [
            models.UniqueConstraint(fields=['league', 'user'], name='unique user entry per league')
        ]

    id = models.AutoField(primary_key=True)
    league = models.ForeignKey(League, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    user_name = models.TextField(null=True, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    prev_position = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('league-standings', args=[str(self.id)])

