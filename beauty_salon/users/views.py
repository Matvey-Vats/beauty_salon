from django.shortcuts import render
from rest_framework import generics

from .models import User
from .serializers import UserSerializer
# Create your views here.


class UserProfileView(generics.ListAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        user = User.objects.filter(id=self.request.user.id)
        return user
    
    def get_serializer_context(self):
        """
        Передаем request в контекст для доступа к текущему пользователю
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
        