from .models import User
from rest_framework import serializers

from services.serializers import AppointmentListSerializer
from services.models import Appointment



class AppointmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения информации о записях
    """
    service_name = serializers.CharField(source='service.name', read_only=True)
    master_name = serializers.CharField(source='master.user.username', read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'service_name', 'master_name', 'date', 'status')
        
    


class UserSerializer(serializers.ModelSerializer):
    
    appointments = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'appointments')
        
        
    def get_appointments(self, obj):
        # Получаем текущего пользователя из контекста запроса
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Фильтруем только те записи, где клиент — это текущий пользователь
            user_appointments = Appointment.objects.filter(client=request.user)
            return AppointmentSerializer(user_appointments, many=True).data
        return []