from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

# urlpatterns = [
#     path('services/', views.ServiceListCreateView.as_view()),
#     path('services/<int:pk>/', views.ServiceDetailView.as_view()),
# ]

urlpatterns = format_suffix_patterns([
    path('services/', views.ServiceListCreateView.as_view()),
    path('services/<int:pk>/', views.ServiceDetailView.as_view()),
    # path('masters/', views.MasterViewSet.as_view({'get': 'list'})),
    path('masters/', views.MasterListView.as_view()),
    path('masters/<int:pk>/', views.MasterDetailView.as_view()),
    path('masters_by_service/<int:service_id>/', views.MasterListByServiceView.as_view()),
    path('appointments/', views.AppointmentListView.as_view()),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view()),
    path('appointments_archive/', views.AppointmentArchiveListView.as_view()),
    
    path('review/', views.ReviewListCreateView.as_view()),
    path('masters/<int:master_id>/schedule/', views.MasterScheduleView.as_view()),
])
