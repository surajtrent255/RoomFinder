from django.urls import reverse_lazy, reverse

from django.views.generic import *
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
# Create your views here.


class BaseMixin(object):  # sab page ma pathaunako lagi, natra dropdown sabai page bata aaudaina
    def get_context_data(Self, **kwargs):
        # maile yo 100 patak vanisake.  #yo buit in method ho over ride gareko hamle.. this method send extra context to client site. jaba hamro html page lai data(category) pathauna parxa taba taba use garne.
        context = super().get_context_data(**kwargs)

        context["latestrooms"] = Room.objects.all().order_by("-id")
        print(context["latestrooms"], "99999999999999999")

        return context


class HomeView(BaseMixin, TemplateView):
    template_name = "normal/home.html"


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


class ClientRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name="ClientGroup").exists():
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

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url

        user = self.request.user
        if user.groups.filter(name="Admin").exists():
            return "/admin/home/"
        elif user.groups.filter(name="LandLord").exists():
            return "/roomlord/home"
        elif user.groups.filter(name="ClientGroup").exists():
            return "/"
        else:
            return "/login/"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class RoomBookView(ClientRequiredMixin, CreateView):
    template_name = "normal/roomBook.html"
    form_class = BookRoomForm
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        room_pk = kwargs["pk"]
        print("roompk%%%%%%%%%%%%%%%", room_pk)
        if request.user.is_authenticated and Client.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/room/"+str(room_pk)+"/detail/")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        room_id = self.kwargs["pk"]
        room = Room.objects.get(id=room_id)
        form.instance.room = room
        loggedin_user = self.request.user
        customer = Client.objects.get(user=loggedin_user)
        form.instance.customer = customer
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        room_id = self.object.room.pk

        return reverse('rentapp:roomDetail', kwargs={'pk': room_id})


class RoomDetailView(DetailView):
    template_name = "normal/roomDetail.html"
    model = Room
    context_object_name = "room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookingStatus = False
        if self.request.user.is_authenticated:
            user = self.request.user
            customer = Client.objects.get(user=user)
            room_id = self.kwargs["pk"]
            room = Room.objects.get(id=room_id)
            bookingList = BookRoom.objects.filter(customer=customer)
            for book in bookingList:
                if book.room == room:
                    bookingStatus = True
        context['bookingStatus'] = bookingStatus
        return context


class CustomerRegistrationView(CreateView):
    template_name = "normal/customerRegistration.html"
    form_class = ClientForm
    success_url = "/login/"

    def form_valid(self, form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        user = User.objects.create_user(uname, "", pword)
        form.instance.user = user
        return super().form_valid(form)


class ClientProfileView(ClientRequiredMixin, TemplateView):
    template_name = "normal/clientProfile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        customer = Client.objects.get(user=user)
        context['customer'] = customer
        return context


class LandLordRegistrationView(CreateView):
    template_name = "normal/landLordRegistration.html"
    form_class = LandLordForm
    success_url = "/login/"

    def form_valid(self, form):
        uname = form.cleaned_data["username"]
        pword = form.cleaned_data["password"]
        user = User.objects.create_user(uname, "", pword)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class BookCancelView(ClientRequiredMixin, View):
    def get(self, request,  *args, **kwargs):
        room_id = kwargs['pk']
        room = Room.objects.get(id=room_id)
        user = request.user
        customer = Client.objects.get(user=user)
        # bookroom object is not iterable if we use get instead of filter" BookRoom can have many booking objects of same user so get method is wrong"
        roomBooks = BookRoom.objects.filter(customer=customer)
        for book in roomBooks:
            if book.room == room:
                book.delete()
        print("before redirect **************************")

        return redirect("/room/"+str(room_id)+"/detail/")
        # if roomBooks.filter(room = room).exists():
