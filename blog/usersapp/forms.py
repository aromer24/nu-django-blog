from django.contrib.auth.forms import UserCreationForm
from .models import BlogUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = BlogUser
        fields = ('username', 'password1', 'password2', 'email')
