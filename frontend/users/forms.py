from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Website


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class WebsiteUpdateForm(forms.ModelForm):
    class Meta:
        model = Website
        fields = ['name', 'use_https']

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Account
