from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    masters = models.ManyToManyField('Master', related_name='services')

    def __str__(self) -> str:
        return self.name
    
class Master(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='master')
    # master_services = models.ManyToManyField(Service)

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
    
    
    def get_end_time(self):
        return self.date + self.service.duration


class AppointmentArchive(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ])
    
    archived_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Archived: {self.client.username} - {self.service.name} with {self.master.user.username} on {self.date}"
    
class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="reviews")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name="reviews")
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Отзыв от {self.client.username} для {self.service.name}"
    
