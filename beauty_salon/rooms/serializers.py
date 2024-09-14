from rest_framework import serializers


from .models import ChatMessage, Room

class ChatMessageSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(slug_field='name', read_only=True)
    sender = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = ChatMessage
        fields = "__all__"
        
        
class ChatMessageCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatMessage
        fields = ["content"]
        

