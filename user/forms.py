from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from user.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password1",
            "password2",
        )


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
        )
