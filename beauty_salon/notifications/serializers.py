from rest_framework import serializers

from .models import Messages



class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model = Messages
        fields = '__all__'
        
