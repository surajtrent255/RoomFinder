
from django.views.generic import *
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
# Create your views here.


class HomeView(TemplateView):
    template_name = "normal/base.html"


class LandLordRequiredMixin(object):
    # hamro new chromema logged in vayerai aauxa, jo paye tesle vitra pasna pauxa.. ctrl+shift+N for chrome. YESLAI FIRST MAI Rakhnu parxa yo function lai
    def dispatch(self, request, *args, **kwargs):
        # function ma request xa vane request.user xaina vane self.request.user.
        user = request.user
        if user.is_authenticated and user.groups.filter(name="LandLord").exists():
            pass
        else:
            return redirect("/login/")

        return super().dispatch(request, *args, **kwargs)


class CustomerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name="Customer").exists():
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name="Admin").exists():
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)


class LoginView(FormView):
    template_name = "normal/login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            login(self.request, usr)

        else:
            return render(self.request, self.template_name,
                          {"error": "login is not  allowed to foreign people",
                           "form": form}
                          )

        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class RoomBookView(CustomerRequiredMixin, CreateView):
    template_name = "clienttemplates/jobapply.html"
    form_class = BookRoomForm
    success_url = "/"

    def form_valid(self, form):
        room_id = self.kwargs["pk"]
        room = Room.objects.get(id=room_id)
        form.instance.room = room
        loggedin_user = self.request.user
        customer = Customer.objects.get(user=loggedin_user)
        form.instance.customer = customer
        return super().form_valid(form)
