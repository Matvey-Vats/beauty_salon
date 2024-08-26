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
        
        
        
class AppointmentListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    master = serializers.SlugRelatedField(slug_field="user.username", read_only=True)
    client = serializers.SlugRelatedField(slug_field="username", read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        
class AppointmentCreateSerializer(serializers.ModelSerializer):
    # client = serializers.ReadOnlyField(source='username')
    class Meta:
        model = Appointment
        fields = ('date', 'service', 'master')
        
