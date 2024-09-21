from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.conf import settings
from django.utils import timezone
import logging

from datetime import datetime, timedelta


from .permissions import IsAdminOrIsSelf
from .utils import ServiceFilter, AppointmentFilter, get_master_schedule

from .serializers import (
    ServiceSerializer,
    ServiceCreateSerializer,
    MasterSerializer,
    MasterCreateSerializer,
    MasterDetailSerializer,
    AppointmentListSerializer,
    AppointmentCreateSerializer,
    AppointmentDetailSerializer,
    ReviewSerializer,
)
from .models import Service, Master, Appointment, AppointmentArchive, Review


logger = logging.getLogger(__name__)

# class ServiceListCreateView(CacheMixin, generics.ListCreateAPIView):
#     queryset = Service.objects.prefetch_related('masters').all()
    
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return ServiceCreateSerializer
#         elif self.request.method == "GET":
#             return ServiceSerializer
        
    
#     def get(self, request, *args, **kwargs):
#         cache_name = 'service_list_cache'
#         cache_time = 60 * 10  # Время жизни кэша (10 минут)

#         # Получаем данные из кэша или из базы данных, если кэша нет
#         data = self.get_cache_data(cache_name)
#         if not data:
#             queryset = self.get_queryset()
#             serializer = self.get_serializer(queryset, many=True)
#             data = serializer.data
#             self.set_cache_data(cache_name, data, cache_time)
        
#         return Response(data)
    
#     def create(self, request, *args, **kwargs):
#         if not request.user.is_staff:
#             logger.warning(f"User {request.user} attempted to create a service but does not have permission.")
#             raise PermissionDenied("Only admins can create services.")
        
#         response = super().create(request, *args, **kwargs)
#         logger.info(f"Service created by {request.user}. Response status: {response.status_code}.")
        
#         self.invalidate_cache("service_list_cache")
#         return response

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.prefetch_related('masters').all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ServiceFilter
    
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ServiceCreateSerializer
        elif self.request.method == "GET":
            return ServiceSerializer
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            logger.warning(f"User {request.user} attempted to create a service but does not have permission.")
            raise PermissionDenied("Only admins can create services.")
        
        response = super().create(request, *args, **kwargs)
        logger.info(f"Service created by {request.user}. Response status: {response.status_code}.")
        return response


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.prefetch_related('masters').all()
    
    def check_staff_permissions(self, request):
        if not request.user.is_staff:
            logger.warning(f"User {request.user} attempted to perform an action on a service but does not have permission.")
            raise PermissionDenied("Only admins can perform this action.")

    def delete(self, request, *args, **kwargs):
        self.check_staff_permissions(request)
        response = super().delete(request, *args, **kwargs)
        logger.info(f"Service deleted by {request.user}. Response status: {response.status_code}.")
        return response

    def update(self, request, *args, **kwargs):
        self.check_staff_permissions(request)
        response = super().update(request, *args, **kwargs)
        logger.info(f"Service updated by {request.user}. Response status: {response.status_code}.")
        return response


    
class MasterListView(generics.ListCreateAPIView):
    queryset = Master.objects.select_related('user').prefetch_related('services').all()
    
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

    
    
class AppointmentListView(generics.ListCreateAPIView):
    queryset = Appointment.objects.select_related('client', 'service', 'master',).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AppointmentFilter
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AppointmentCreateSerializer
        return AppointmentListSerializer
        
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
        
class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.select_related('client', 'service', 'master').all()
    serializer_class = AppointmentDetailSerializer
    
    
class AppointmentArchiveListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        # Статистика по количеству завершенных услуг для каждого клиента
        stats = AppointmentArchive.objects.values('client__username').annotate(total_services=Count('id')).order_by('-total_services')

        return Response(stats)
    
    
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
        

class MasterScheduleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, master_id, *args, **kwargs):
        try:
            master = Master.objects.get(id=master_id)
        except Master.DoesNotExist:
            return Response({"error": "Master not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
        schedule = get_master_schedule(master)
        
        return Response(schedule, status=status.HTTP_200_OK)