from rest_framework import serializers
from .models import Room

#what does a serializer do? 
#a serializer is basically the translater between django model and json 

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class meta:
        model = Room
        fields = ['url', 'id', 'name', 'room_type', 'pricePerNight', 'currency', 'maxOccupancy', 'description']