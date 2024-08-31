from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .permissions import IsAdminOrIsSelf

from .serializers import (
    ServiceSerializer,
    ServiceCreateSerializer,
    MasterSerializer,
    MasterCreateSerializer,
    MasterDetailSerializer,
    AppointmentListSerializer,
    AppointmentCreateSerializer,
    AppointmentDetailSerializer,
)
from .models import Service, Master, Appointment


class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.prefetch_related('masters').all()
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ServiceCreateSerializer
        elif self.request.method == "GET":
            return ServiceSerializer
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("Only admins can create services.")
        return super().create(request, *args, **kwargs)
    
    
    

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.prefetch_related('masters').all()
    
    def check_staff_permissions(self, request):
        if not request.user.is_staff:
            raise PermissionDenied("Only admins can perform this action.")

    def delete(self, request, *args, **kwargs):
        self.check_staff_permissions(request)
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.check_staff_permissions(request)
        return super().update(request, *args, **kwargs)
    

# class MasterViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = MasterSerializer
#     queryset = Master.objects.select_related('user').all()
    
class MasterListView(generics.ListCreateAPIView):
    queryset = Master.objects.select_related('user').all()
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return MasterCreateSerializer
        return MasterSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class MasterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Master.objects.select_related('user').all()
    permission_classes = (IsAdminOrIsSelf,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MasterSerializer
        return MasterDetailSerializer
    


class MasterListByServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, service_id):
        masters = Master.objects.select_related('user').filter(services__id=service_id)
        return Response([{'id': master.id, 'username': master.user.username} for master in masters])

# class AppointmentViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = AppointmentSerializer
#     queryset = Appointment.objects.all()
    
    
class AppointmentListView(generics.ListCreateAPIView):
    queryset = Appointment.objects.select_related('client', 'service', 'master').all()
    
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AppointmentCreateSerializer
        return AppointmentListSerializer
        
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
        
class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.select_related('client', 'service', 'master').all()
    serializer_class = AppointmentDetailSerializer