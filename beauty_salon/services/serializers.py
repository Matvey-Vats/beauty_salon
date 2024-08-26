from rest_framework import serializers

from .models import Service, Master, Appointment

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("__all__")
        

class MasterSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    services = ServiceSerializer(read_only=True, many=True)
    
    class Meta:
        model = Master
        fields = '__all__'