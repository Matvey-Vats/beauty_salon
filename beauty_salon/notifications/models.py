from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Messages(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="messages")
    content = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.content