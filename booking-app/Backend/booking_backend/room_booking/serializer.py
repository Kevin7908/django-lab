from rest_framework import serializers
from .models import Room, RoomImage, OccupiedDate, User

#what does a serializer do? 
#a serializer is basically the translater between django model and json 

class RoomImagesSerializer(serializers.ModelSerializer):
    room = serializers.HyperlinkedRelatedField(view_name = 'room-detail', queryset = Room.objects.all())
    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'caption', 'room']

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    images = RoomImagesSerializer(many = True, read_only = True) 
    class Meta:
        model = Room
        fields = ['url', 'id', 'name', 'room_type', 'pricePerNight', 'currency', 'maxOccupancy', 'description', 'images']

class OccupiedDateSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        view_name = 'room-detail',
        queryset = Room.objects.all()
        )
    class Meta:
        model = OccupiedDate
        fields = ['url', 'id', 'room', 'date']

from django.contrib.auth.hashers import make_password
class UserSerealizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'email', 'full_name']
        # La contraseña solo se recibe, nunca se devuelve en las respuestas
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        return make_password(value)

# --- Serializers usados solo para documentar (OpenAPI) ---
# Login y Register devuelven un diccionario armado a mano, así que DRF no puede
# deducir su forma. Estos serializers describen ese contrato para el esquema.

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.EmailField(help_text='Email del usuario')
    password = serializers.CharField(write_only=True)

class AuthUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.EmailField()
    email = serializers.EmailField()
    full_name = serializers.CharField()

class AuthResponseSerializer(serializers.Serializer):
    user = AuthUserSerializer()
    token = serializers.CharField(help_text='Usar en el header: Authorization: Token <token>')
