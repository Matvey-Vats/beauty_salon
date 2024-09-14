from django.db import models
from django.contrib.auth import get_user_model
from services.models import Master

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="client_rooms")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name="master_rooms")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Room: {self.name} between {self.client.username} and {self.master.user.username}"
    
    
class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')  # Связь с моделью Room
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Кто отправил сообщение
    content = models.TextField()  # Текст сообщения
    timestamp = models.DateTimeField(auto_now_add=True)  # Время отправки сообщения

    def __str__(self):
        return f"Message from {self.sender.username} in room {self.room.name} at {self.timestamp}"