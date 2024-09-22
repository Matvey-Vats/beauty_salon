from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, RegisterSerializer
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
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)