from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Введите email.')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='Введите пароль')
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, help_text='Введите пароль еще раз')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

class UserAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Введите email.')
    password = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='Введите пароль')
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, help_text='Введите пароль еще раз')

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')
