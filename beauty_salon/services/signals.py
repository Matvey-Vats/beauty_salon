from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment

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
