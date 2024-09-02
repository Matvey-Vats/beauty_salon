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
        
@shared_task
def update_appointment_status():
    from .models import Appointment
    """
    Периодическая задача для обновления статуса записей.
    """
    # Получаем текущую дату и время
    now = timezone.now()

    # Ищем все записи, у которых статус 'scheduled' и дата уже прошла
    appointments = Appointment.objects.filter(status='scheduled', date__lt=now)

    # Обновляем статус записей
    for appointment in appointments:
        appointment.status = 'completed'
        appointment.save()
        

@shared_task
def archive_old_appointments():
    from .models import Appointment, AppointmentArchive
    
    now = timezone.now()
    
    old_appointments = Appointment.objects.filter(
        status__in=['completed', 'canceled'],
        date__lt=now
    )
    
    for appointment in old_appointments:
        AppointmentArchive.objects.create(
            service=appointment.service,
            master=appointment.master,
            client=appointment.client,
            date=appointment.date,
            status=appointment.status,
        )
        
        appointment.delete()
        
    return f"Archived {len(old_appointments)} appointments"