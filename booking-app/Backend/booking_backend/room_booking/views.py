from django.shortcuts import render
from rest_framework import generics 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Room 
from .serializer import RoomSerializer

# Create your views here.
@api_view(['GET']) 
def api_root(request, format=None):
    return Response({
        'rooms':reverse('room-list', request=request, format=format)
    })

class RoomList (generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer