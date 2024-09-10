from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from services.models import Appointment, Service, Master
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse_lazy

class AppointmentAPITest(APITestCase):
    def setUp(self):
        self.client_user = get_user_model().objects.create(
            username="client",
            password="password1234"
        )
        
        self.master_user = get_user_model().objects.create(
            username="master",
            password="password1234"
        )
        
        self.master = Master.objects.create(user=self.master_user)
        
        self.service = Service.objects.create(
            name='Haircut',
            description='Professional haircut service',
            price=100,
            duration="00:30:00"
        )
        
        self.appointment_url = "/api/v1/appointments/"
        
        
    def test_create_appointment(self):
        self.client.force_authenticate(user=self.client_user)
        data = {
            'service': self.service.id,
            'master': self.master.id,
            'client': self.client_user.id,
            'date': timezone.now(),
            'status': 'scheduled'
        }
        
        response = self.client.post(self.appointment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertEqual(Appointment.objects.first().client, self.client_user)
        
    
    def test_get_appointments(self):
        self.client.force_authenticate(user=self.client_user)
        
        appointment = Appointment.objects.create(
            service=self.service,
            master=self.master,
            client=self.client_user,
            date=timezone.now(),
            status='scheduled'
        )
        
        response = self.client.get(self.appointment_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], appointment.id)