from django.db import models

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
