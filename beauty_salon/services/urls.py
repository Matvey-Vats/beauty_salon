from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('services/', views.ServiceListCreateView.as_view()),
    path('services/<int:pk>/', views.ServiceDetailView.as_view()),
]

urlpatterns = format_suffix_patterns([
    path('masters/', views.MasterViewSet.as_view({'get': 'list'})),
    path('masters/<int:pk>/', views.MasterViewSet.as_view({'get': 'retrieve'})),
    
])
