from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    def __str__(self) -> str:
        return self.name
    
class Master(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='master')
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.user.username
    
    
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name="appointments")
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="appointments")
    date = models.DateTimeField()  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="scheduled")
    
    def __str__(self):
        return f"{self.client.username} - {self.service.name} with {self.master.user.username} on {self.date}"  


