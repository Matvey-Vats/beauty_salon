from django.shortcuts import render
from rest_framework import generics


from .models import Messages
from .serializers import MessageSerializer

class MessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        queryset = Messages.objects.select_related('user').filter(user=self.request.user)
        
        queryset.filter(is_read=False).update(is_read=True)
        
        return queryset