from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .serializers import ServiceSerializer

from .models import Service


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admins can create services.")
        return super().create(request, *args, **kwargs)
    

