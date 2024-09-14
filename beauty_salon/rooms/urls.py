from django.urls import path

from . import views

urlpatterns = [
    path('chat/room/<str:room_name>/messages/', views.ChatMessageAPIView.as_view()),
]
