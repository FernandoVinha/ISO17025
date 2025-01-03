from django.urls import path
from . import views
from .views import *

# Adicione o namespace do app
app_name = 'locations'

urlpatterns = [
    # ====== Building URLs ======
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/create/', views.building_create, name='building_create'),
    path('buildings/edit/<int:pk>/', views.building_edit, name='building_edit'),
    path('buildings/delete/<int:pk>/', views.building_delete, name='building_delete'),

    # ====== Room URLs ======
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/edit/<int:pk>/', views.room_edit, name='room_edit'),
    path('rooms/delete/<int:pk>/', views.room_delete, name='room_delete'),

    # ====== Measurement URLs ======
    path('measurements/', views.measurement_room_list, name='measurement_room_list'),
    path('measurements/room/<int:pk>/', views.measurement_room_detail, name='measurement_room_detail'),
    path('measurements/create/', views.measurement_create, name='measurement_create'),

    # ====== API URLs ======
    path('api/create-room-measurement/', create_room_and_measurement, name='create_room_measurement'),
    path('api/measurements/<int:room_id>/', views.get_measurements_data, name='get_measurements_data'),
]
