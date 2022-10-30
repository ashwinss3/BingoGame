from django.contrib.auth.forms import UserCreationForm
from bingo.models import User


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

