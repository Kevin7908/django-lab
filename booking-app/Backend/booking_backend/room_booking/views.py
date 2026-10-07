from django.shortcuts import render
from rest_framework import generics 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from .permissions import IsAdminOrReadOnly
from rest_framework import permissions
from .models import Room, OccupiedDate, User
from .serializer import RoomSerializer, OccupiedDateSerializer, UserSerealizer
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers
from .serializer import LoginRequestSerializer, AuthResponseSerializer

# Create your views here.
@extend_schema(
    tags=['root'],
    summary='Punto de entrada de la API',
    responses=inline_serializer('ApiRoot', fields={'rooms': serializers.URLField()}),
)
@api_view(['GET']) 
def api_root(request, format=None):
    return Response({
        'rooms':reverse('room-list', request=request, format=format)
    })

@extend_schema(tags=['rooms'])
class RoomList (generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

# RetrieveUpdateDestroyAPIView it gives to my api three operations automatically get, put/patch, delete
@extend_schema(tags=['rooms'])
class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

@extend_schema(tags=['occupied-dates'])
class OccupiedDatesList (generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        user = self.request.user

        if not user.is_superuser and not user.is_staff:
            OccupiedDate.objects.filter(user = user)

        return super().get_queryset()

# RetrieveUpdateDestroyAPIView it gives to my api three operations automatically get, put/patch, delete
@extend_schema(tags=['occupied-dates'])
class OccupiedDatesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [IsAdminOrReadOnly]

# 'ListAPIView' is a built-in DRF generic view that handles HTTP GET requests 
# for a COLLECTION (list) of objects. Instead of returning one specific item, 
# it returns a list of items as a JSON array. It is read-only (no creating/POST).
@extend_schema(tags=['users'])
class UserList(generics.ListAPIView):
    # This is the default base list of objects the view will look at.
    queryset = User.objects.all()
    
    # This tells the view how to translate the User models into JSON.
    serializer_class = UserSerealizer # (Note: usually spelled UserSerializer)

    # 'get_queryset' is the behind-the-scenes method ListAPIView uses to figure out 
    # WHICH items belong in the list before sending them to the user. 
    # By overriding it, we can dynamically filter the results.
    def get_queryset(self):
        # 1. Identify who is making the request (the currently logged-in user).
        user = self.request.user

        # 2. Check if the user is a staff member or an admin.
        if user.is_staff or user.is_superuser:
            # If they are an admin, give them the full list of ALL users in the database.
            return User.objects.all()
        else:
            # 3. If they are a regular user, filter the list so it only contains their own profile.
            # FIX: I changed 'user = user.id' to 'id = user.id'. 
            # Since you are querying the User model, you have to search by its 'id' field!
            return User.objects.filter(id=user.id)


# 'RetrieveAPIView' is a built-in DRF generic view that handles HTTP GET requests 
# for a single object. It automatically takes the ID from the URL (like /users/1/), 
# searches the database for it, and returns the data as JSON. 
# It provides a "read-only" detail endpoint (no updating or deleting).
@extend_schema(tags=['users'], responses={200: UserSerealizer, 403: OpenApiResponse(description='No es tu usuario ni eres staff')})
class UserDetail(generics.RetrieveAPIView):
    # This tells the view where to look for the object in the database.
    queryset = User.objects.all()
    
    # This tells the view how to translate the User model into JSON.
    serializer_class = UserSerealizer

    # 'get_object' is the behind-the-scenes method RetrieveAPIView uses to grab the specific 
    # item from the database. By overriding it here, we can add custom permission checks 
    # before we hand the data back to the user.
    def get_object(self):
        # 1. Identify who is making the request (the currently logged-in user).
        user = self.request.user
        
        # 2. Call the default Django behavior to fetch the requested User profile from the DB.
        # (Note: I added () after super here, which is required in Python)
        obj = super().get_object() 
        
        # 3. Check permissions: Are they trying to view their OWN profile? 
        # Or are they an admin/staff member?
        if obj == user or user.is_staff or user.is_superuser:
            # If yes, allow them to see the data!
            return obj
        else:
            raise PermissionDenied("You do no thave permission to access this user's detail. ")

###### lil bro this so important, check this out #######################
"""
--- QUICK REFERENCE: get_object() vs get_queryset() ---

get_object():
- Used in views that handle a SINGLE item (like RetrieveAPIView, UpdateAPIView, DestroyAPIView).
- It uses the ID in the URL (e.g., /users/5/) to grab one specific item from the database.
- OVERRIDE THIS when you want to check permissions or run custom logic on ONE specific 
  object before giving it to the user. (e.g., "Can this user view this specific profile?")

get_queryset():
- Used in views that handle MULTIPLE items (like ListAPIView) to return a list.
- It determines the base collection of items the view is allowed to look at.
- OVERRIDE THIS when you want to filter a database table so the user only sees a 
  restricted list of items. (e.g., "Only return a list of posts created by this user.")
"""

@extend_schema(
    tags=['auth'],
    summary='Registrar un usuario nuevo',
    request=UserSerealizer,
    responses={200: AuthResponseSerializer},
)
class Register (generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerealizer

    def perform_create(self, serializer):
        user = serializer.save()

        token, created = Token.objects.get_or_create(user = user)

        self.response_data = {
            'user': {
                'id': user.id,
                'username': user.email,
                'email': user.email,
                'full_name': user.full_name
            },
            'token': token.key
        } 

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(self.response_data)

@extend_schema(
    tags=['auth'],
    summary='Iniciar sesión con email y contraseña',
    request=LoginRequestSerializer,
    responses={
        200: AuthResponseSerializer,
        401: OpenApiResponse(description='Credenciales inválidas'),
    },
    auth=[],  # endpoint público: no requiere autenticación
)
class Login (APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username = username, password = password)
        if user is None:
            raise AuthenticationFailed('Invalid username or password')

        token, created = Token.objects.get_or_create(user = user)

        return Response({
                    'user': {
                        'id': user.id,
                        'username': user.email,
                        'email': user.email,
                        'full_name': user.full_name
                    },
                    'token': token.key
                })