from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .models import Appointment, Service

@receiver(post_save, sender=Appointment)
def send_appointment_email(sender, instance, created, **kwargs):
    if created:
        # Отправка письма
        send_mail(
            subject='Новая запись на услугу',
            message=f'Уважаемый {instance.client.username}, вы записаны на {instance.service.name} в {instance.date}.',
            from_email='noreply@example.com',
            recipient_list=[instance.client.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Service)
@receiver(post_delete, sender=Service)
def clear_service_cache(sender, **kwargs):
    cache_name = 'service_list_cache'
    cache.delete(cache_name)