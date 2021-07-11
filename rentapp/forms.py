from django import forms
from django.db.models import fields
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class BookRoomForm(forms.ModelForm):
    class Meta:
        model = BookRoom
        fields = ['citizenship_front', 'citizenship_back']


class ClientForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Client
        fields = ["username", "password", "confirm_password",
                  "full_name", "email", "mobile"]

    def clean_username(self):
        uname = self.cleaned_data["username"]
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("This username is already taken")

        return uname

    def clean_confirm_password(self):
        pword = self.cleaned_data["password"]
        c_pword = self.cleaned_data["confirm_password"]
        if(pword != c_pword):
            raise forms.ValidationError(
                "Hey, Foolish type password carefully!!!")

        return c_pword


class LandLordForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = LandLord
        fields = ["username", "password", "confirm_password",
                  "full_name", "mobile", "email", "phone", "adress"]

    def clean_username(self):
        uname = self.cleaned_data["username"]
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("This username is already taken")

        return uname

    def clean_confirm_password(self):
        pword = self.cleaned_data["password"]
        c_pword = self.cleaned_data["confirm_password"]
        if(pword != c_pword):
            raise forms.ValidationError(
                "Hey, Foolish type password carefully!!!")

        return c_pword
