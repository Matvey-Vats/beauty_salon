from django.contrib import admin

# Register your models here.
from .models import Service, Master, Appointment, AppointmentArchive

admin.site.register(Service)
admin.site.register(Master)
admin.site.register(Appointment)
admin.site.register(AppointmentArchive)