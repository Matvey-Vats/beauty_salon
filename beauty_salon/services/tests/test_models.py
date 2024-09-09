from django.test import TestCase
from services.models import Service, Appointment, Master
from django.contrib.auth import get_user_model
from django.utils import timezone

class ServiceTestCase(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Haircut",
            description="A simple haircut service",
            price=20.00,
            duration="00:30:00"
        )
        
        
    def test_service_creation(self):
        service = self.service
        self.assertTrue(isinstance(service, Service))
        self.assertEqual(service.__str__(), service.name)
        
    
    def test_service_price(self):
        service = self.service
        self.assertEqual(service.price, 20.00)
        
        
    def test_service_str_method(self):
        service = self.service
        self.assertEqual(str(service), "Haircut")
        
        
    def test_service_update(self):
        service = self.service
        service.name = "New Haircut"
        service.save()
        self.assertEqual(service.name, "New Haircut")
        
    def test_service_delete(self):
        service = self.service
        service_id = service.id
        service.delete()
        with self.assertRaises(Service.DoesNotExist):
            Service.objects.get(id=service_id)
        
class AppointmentTestCase(TestCase):
    def setUp(self) -> None:
        self.service = Service.objects.create(
            name="Haircut",
            description="A simple haircut service",
            price=20.00,
            duration="00:30:00"
        )
        
        self.master_user = get_user_model().objects.create(
            username="masteruser",
            password="password1234"
        )
        
        self.client = get_user_model().objects.create(
            username="client",
            password="password1234"
        )
        
        self.master = Master.objects.create(
            user=self.master_user
        )
        
        self.appointment = Appointment.objects.create(
            service=self.service,
            master=self.master,
            client=self.client,
            date=timezone.now(),
            status="scheduled"
        )
        
    def test_appointment_creation(self):
        
        self.assertEqual(self.appointment.client, self.client)
        self.assertEqual(self.appointment.master, self.master)
        self.assertEqual(self.appointment.service, self.service)
        self.assertEqual(self.appointment.status, 'scheduled')
        self.assertIsNotNone(self.appointment.date)
        self.assertEqual(str(self.appointment), f"{self.client.username} - {self.service.name} with {self.master.user.username} on {self.appointment.date}")
    
    def test_appointment_status_change(self):
        """Тестируем изменение статуса записи."""
        self.appointment.status = 'completed'
        self.appointment.save()
        self.assertEqual(self.appointment.status, 'completed')

    def test_appointment_deletion(self):
        """Тестируем удаление записи."""
        self.appointment.delete()
        self.assertEqual(Appointment.objects.count(), 0)