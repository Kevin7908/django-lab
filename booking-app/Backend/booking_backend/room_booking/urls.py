from django.urls import path
from room_booking import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('rooms/', views.RoomList.as_view(), name='room-list'),
    # this define the url pattern 'rooms/<int:pk>', as_view() converts that class into something Django's URL system can call when a request arrives.
    path('rooms/<int:pk>/', views.RoomDetail.as_view(), name='room-detail'),
    path('occupied-dates/', views.OccupiedDatesList.as_view(), name='occupieddate-list'),
    path('occupied-dates/<int:pk>/', views.OccupiedDatesDetail.as_view(), name='occupieddate-detail'),
    path('user/', views.UserList.as_view(), name = 'user-list'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name = 'user-detail'),
    path('login/', views.Login.as_view(), name = 'login'),
    path('register/', views.Register.as_view(), name = 'register'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)