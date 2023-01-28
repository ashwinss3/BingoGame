import traceback

from django.contrib.auth.forms import UserCreationForm
from bingo.models import User
from allauth.socialaccount.forms import SignupForm


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomSocialSignupForm(SignupForm):
    """
    Custom Signup Form which will be shown when user signs up via Social Account.
    Used to select/change username for the user.
    """
    def __init__(self, *args, **kwargs):
        super(CustomSocialSignupForm, self).__init__(*args, **kwargs)
        values_from_social = self.__get_details_from_social(kwargs.get('sociallogin'))
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

            # if the value is already present from social login data then using that
            if values_from_social.get(visible.name):
                visible.initial = values_from_social[visible.name]

    def __get_details_from_social(self, social_obj):
        try:
            if not social_obj or not hasattr(social_obj, 'user'):
                return {}

            default_details = {}
            default_details['username'] = getattr(social_obj.user, 'username') or \
                                          getattr(social_obj.user, 'first_name')
            default_details['email'] = getattr(social_obj.user, 'email')
            return default_details

        except Exception as ex:
            traceback.format_exc()
            return {}

    def save(self, request):
        user = super(CustomSocialSignupForm, self).save(request)
        return user

