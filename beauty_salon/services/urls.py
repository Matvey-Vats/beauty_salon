from django.urls import path
from . import views

urlpatterns = [
    path('services/', views.ServiceListCreateView.as_view()),
]
