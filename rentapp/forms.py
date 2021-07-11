from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class BookRoomForm(forms.ModelForm):
    class Meta:
        model = BookRoom
