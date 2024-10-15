# locations/admin.py

from django.contrib import admin
from .models import Building, Room, Measurement

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'responsible_user')
    search_fields = ('name', 'address')
    list_filter = ('responsible_user',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor', 'building', 'capacity', 'responsible_user')
    search_fields = ('name', 'building__name')
    list_filter = ('building', 'floor', 'responsible_user')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('room', 'temperature', 'humidity', 'recorded_at')
    search_fields = ('room__name',)
    list_filter = ('room', 'recorded_at')
