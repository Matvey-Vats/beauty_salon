from celery import shared_task
from django.utils import timezone

@shared_task
def delete_readed_notification(self):
    ...