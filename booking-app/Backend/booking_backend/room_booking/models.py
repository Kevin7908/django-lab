from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

#This how we created a model in django
class Room(models.Model):
    #This is basically a list of choises
    # so teh first value is gonna be the database value and the second one is the displayed value
    ROOM_TYPES = [
        ('suite', 'Suite'),
        ('standart', 'Standar Room'),
        ('deluxe', 'Deluxe Room')
    ]

    CURRENCY_TYPES= [
        ('USD', 'USD'),
        ('COP', 'COP')
    ]

    #blank=True makes the field optional
    name = models.CharField(max_length=100, blank=True, default='')
    #choises=ROOM_TYPES i'm telling to djago this field can only have one of the option of ROOM_TYPES
    room_type = models.CharField(max_length=100, choices=ROOM_TYPES)
    pricePerNight = models.IntegerField(default=150)
    currency = models.CharField(default='USD', max_length=10, choices=CURRENCY_TYPES)
    maxOccupancy = models.IntegerField(default=1)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.name} ({self.room_type})"

class RoomImage(models.Model):
    # Stores the image file associated with a room.
    # Uploaded images will be placed inside the "room_images/" directory.
    image = models.ImageField(upload_to="room_images/")

    # Optional text describing the image.
    # blank=True allows it to be empty in forms.
    # null=True allows the database to store NULL.
    caption = models.CharField(max_length=255, blank=True, null=True)

    # Connects this image to a specific Room.
    # A room can have multiple images because of related_name="images".
    # If the room is deleted, all its images are deleted as well.
    room = models.ForeignKey(Room, related_name="images", on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for: {self.room.name} - {self.caption or 'no caption'}"

class OccupiedDate(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="ocupiedDates")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='booked_dates')
    date = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.room.name} booked by {self.user.username}"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, default='')