from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .models import Appointment, Service
from notifications.models import Messages
from django.db import transaction

from .utils import send_notification_email

@receiver(post_save, sender=Appointment)
def send_appointment_email(sender, instance, created, **kwargs):
    if created:
        client_message = f'Уважаемый {instance.client.username}, вы записаны на {instance.service.name} в {instance.date}.'
        master_message = f'Уважаемый {instance.master.user.username}, у вас запись на {instance.service.name} в {instance.date}.'
        
        # Используем транзакцию, чтобы гарантировать целостность данных
        with transaction.atomic():
            # Отправляем email клиенту и мастеру
            send_notification_email(
                subject='Новая запись на услугу',
                message=client_message,
                recipient_list=[instance.client.email]
            )
            send_notification_email(
                subject='Новая запись на услугу',
                message=master_message,
                recipient_list=[instance.master.user.email]
            )
            
            # Создаем сообщения для системы уведомлений
            Messages.objects.create(user=instance.client, content=client_message)
            Messages.objects.create(user=instance.master.user, content=master_message)






# @receiver(post_save, sender=Service)
# @receiver(post_delete, sender=Service)
# def clear_service_cache(sender, **kwargs):
#     cache_name = 'service_list_cache'
#     cache.delete(cache_name)