from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Admin(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.CharField(max_length=200)
    image = models.ImageField(upload_to="admin")
    adress = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):  # save already xa extra logic lekheko
        group, created = Group.objects.get_or_create(name="Admin")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class LandLord(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, null=True, blank=True)
    adress = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="LandLord")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Customer(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):  # save already xa extra logic lekheko
        group, created = Group.objects.get_or_create(name="Customer")
        self.user.groups.add(group)
        super().save(*args, **kwargs)


class Room(TimeStamp):
    title = models.CharField(max_length=200)
    landLord = models.ForeignKey(LandLord, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room", null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class BookRoom(TimeStamp):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.room.title
