
from django.contrib import admin
from django.urls import path
from .views import *
app_name = "rentapp"


urlpatterns = [
    path('', HomeView.as_view(), name="home"),


]
