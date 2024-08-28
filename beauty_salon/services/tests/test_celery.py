# meetings/tests/tasks_tests.py

from django.test import TestCase
from unittest.mock import patch
from django.core import mail
from django.utils import timezone
from datetime import timedelta
from services.models import Service, Master, Appointment
from services.tasks import send_appointment_reminder

class TaskTests(TestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Создаем пользователей
        self.client_user = User.objects.create_user(username='client', email='client@example.com', password='clientpassword')
        self.master_user = User.objects.create_user(username='master', email='master@example.com', password='masterpassword')

        # Создаем сервис
        self.service = Service.objects.create(
            name='Service 1',
            description='Description of service 1',
            price=100.00,
            duration='01:00:00'
        )

        # Создаем мастера и связываем его с сервисом
        self.master = Master.objects.create(user=self.master_user)
        self.master.master_services.add(self.service)

        # Создаем запись, которая должна быть напомнена
        self.appointment = Appointment.objects.create(
            service=self.service,
            master=self.master,
            client=self.client_user,
            date=timezone.now() + timedelta(days=1),  # Напоминание будет отправлено завтра
            status='scheduled'
        )

    @patch('django.core.mail.send_mail')
    def test_send_appointment_reminder(self, mock_send_mail):
        # Запускаем задачу Celery
        send_appointment_reminder.apply_async()

        # Подождем, пока задача выполнится
        from time import sleep
        sleep(1)  # Период ожидания можно настроить по необходимости

        # Проверяем, что функция отправки писем была вызвана
        mock_send_mail.assert_called_once()
        args, kwargs = mock_send_mail.call_args
        self.assertEqual(args[0], 'Напоминание о записи')
        self.assertIn('Напоминаем вам о записи на услугу', args[1])
        self.assertEqual(args[3], [self.client_user.email])
