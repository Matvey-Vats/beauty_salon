from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Room, ChatMessage
from .serializers import ChatMessageSerializer, ChatMessageCreateSerializer



# class ChatMessageAPIView(APIView):
    
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, room_name):
        
#         room = Room.objects.get(name=room_name)
        
#         last_timestamp = request.query_params.get('last_timestamp')
        
#         if last_timestamp:
#             last_timestamp = timezone.datetime.fromisoformat(last_timestamp)
#             messages = ChatMessage.objects.filter(room=room, timestamp__gt=last_timestamp)
        
#         else:
#             messages = ChatMessage.objects.filter(room=room).order_by('-timestamp')[:50]
            
#         serializer = ChatMessageSerializer(messages, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, room_name):
#         room = Room.objects.get(name=room_name)
#         content = request.data.get('content')
        
#         message = ChatMessage.objects.create(
#             room=room,
#             sender=request.user,
#             content=content,
#         )
        
#         serializer = ChatMessageSerializer(message)
#         return Response(serializer.data, status=201)
    


    
class ChatMessageAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        
        room_name = self.kwargs['room_name']
        room = Room.objects.get(name=room_name)

    
        last_timestamp = self.request.query_params.get('last_timestamp')
        
        if last_timestamp:
            last_timestamp = timezone.datetime.fromisoformat(last_timestamp)
            return ChatMessage.objects.filter(room=room, timestamp__gt=last_timestamp)
        else:
            return ChatMessage.objects.filter(room=room).order_by('-timestamp')[:50]
        
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ChatMessageSerializer
        else:
            return ChatMessageCreateSerializer
    
    def perform_create(self, serializer):
        room_name = self.kwargs['room_name']
        room = Room.objects.get(name=room_name)
        
        serializer.save(room=room, sender=self.request.user)     