# locations/serializers.py

from rest_framework import serializers
from .models import Room, Measurement

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'floor', 'building', 'capacity']

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['room', 'temperature', 'humidity']
