from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view()),
    path('register/', views.RegisterView.as_view()),
]
