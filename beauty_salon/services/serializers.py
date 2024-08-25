from rest_framework import serializers

from .models import Service, Master, Appointment

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("__all__")