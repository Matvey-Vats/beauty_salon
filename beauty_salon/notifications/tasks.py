from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task
def delete_readed_notification():
    from notifications.models import Messages
    
    now = timezone.now()
    msgs = Messages.objects.filter(is_read=True)
    for msg in msgs:
        msg.delete()
    