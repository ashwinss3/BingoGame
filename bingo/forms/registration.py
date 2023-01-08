from django.contrib.auth.forms import UserCreationForm
from bingo.models import User


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


