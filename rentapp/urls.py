
from django.contrib import admin
from django.urls import path
from .views import *
app_name = "rentapp"


urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path("room/<int:pk>/detail/", RoomDetailView.as_view(), name="roomDetail"),
    path("room/<int:pk>/book/", RoomBookView.as_view(), name="roombook"),

    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("customer/registration/", CustomerRegistrationView.as_view(),
         name="customerRegistration"),
    path("landLord/registration/", LandLordRegistrationView.as_view(),
         name="landLordRegistration"),
    path("client/profile/", ClientProfileView.as_view(), name="clientprofile"),
    path("book/<int:pk>/cancel/", BookCancelView.as_view(), name="bookcancel"),

    path("roomlord/home/", RoomLordHOmeView.as_view(), name="roomLordhome"),
    path("roomlord/room/", RoomLordRoomsView.as_view(), name="roomlordrooms"),
    path("roomLord/add/room/", AddRoomByRoomLordView.as_view(),
         name="addRoomByRoomLord"),
    path("roomLord/<int:pk>/update/room/",
         UpdateRoomByRoomLordView.as_view(), name="roomlordupdaterooms"),
    path("roomLord/<int:pk>/delete/room/",
         DeleteRoomByRoomLordView.as_view(), name="roomlorddeleterooms"),







]
