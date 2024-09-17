from django.urls import path

from . import views

urlpatterns = [
    path('chat/room/<str:room_name>/messages/', views.ChatMessageAPIView.as_view()),
    path('chat/room/', views.RoomListCreateView.as_view()),
]
