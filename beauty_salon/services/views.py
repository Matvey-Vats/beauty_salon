from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .serializers import ServiceSerializer, MasterSerializer

from .models import Service, Master


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admins can create services.")
        return super().create(request, *args, **kwargs)
    

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    
    def check_staff_permissions(self, request):
        if not request.user.is_staff:
            raise PermissionDenied("Only admins can perform this action.")

    def delete(self, request, *args, **kwargs):
        self.check_staff_permissions(request)
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.check_staff_permissions(request)
        return super().update(request, *args, **kwargs)
    

class MasterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MasterSerializer
    queryset = Master.objects.all()
