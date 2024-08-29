from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_appointment_reminder():
    from .models import Appointment
    
    
    now = timezone.now()
    reminder_time = now + timedelta(days=1)
    appointments = Appointment.objects.filter(date__date=reminder_time.date(), status='scheduled')
    
    for appointment in appointments:
        send_mail(
            'Напоминание о записи',
            f'{appointment.client.username} напоминаем вам о записи на услугу "{appointment.service.name}" завтра ({appointment.date}).',
            'from@example.com',
            [appointment.client.email],
            fail_silently=False,
        )