
from django.contrib import admin
from .models import *

admin.site.register([Admin, LandLord, Room, BookRoom, Client])
