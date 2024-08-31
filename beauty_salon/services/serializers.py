from rest_framework import serializers

from .models import Service, Master, Appointment

class ServiceSerializer(serializers.ModelSerializer):
    masters = serializers.SerializerMethodField()


    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'masters']

    def create(self, validated_data):
        masters = validated_data.pop('masters', [])
        service = Service.objects.create(**validated_data)
        service.masters.set(masters)
        return service

    def update(self, instance, validated_data):
        masters = validated_data.pop('masters', [])
        instance = super().update(instance, validated_data)
        instance.masters.set(masters)
        return instance
    
    def get_masters(self, obj):
        return [master.user.username for master in obj.masters.all()]

class ServiceCreateSerializer(serializers.ModelSerializer):
    
    masters = serializers.PrimaryKeyRelatedField(
        queryset=Master.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'masters']

    def create(self, validated_data):
        masters = validated_data.pop('masters', [])
        service = Service.objects.create(**validated_data)
        service.masters.set(masters)
        return service
        

class MasterSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    services = ServiceSerializer(read_only=True, many=True)
    
    class Meta:
        model = Master
        fields = '__all__'
        
class MasterCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = Master
        fields = ('user',)
        
class MasterDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    # services = ServiceSerializer(read_only=True, many=True)
    
    class Meta:
        model = Master
        fields = ('user', 'services')
        
        
        
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
        
    def validate(self, data):
        service = data.get('service')
        master = data.get('master')

        if master and service and not master.services.filter(id=service.id).exists():
            raise serializers.ValidationError("Этот мастер не предлагает выбранную услугу.")
        
        return data
    
class AppointmentDetailSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(slug_field="name", read_only=True)
    master = serializers.SlugRelatedField(slug_field="user.username", read_only=True)
    client = serializers.SlugRelatedField(slug_field="username", read_only=True)
    
    class Meta:
        model = Appointment
        fields = ('date', 'service', 'master', 'client', 'status')
        
    
