from django import forms
from .models import UserPost
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['title', 'content_text', 'content_file']


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']