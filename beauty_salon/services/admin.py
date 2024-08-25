from django.contrib import admin

# Register your models here.
from .models import Service, Master, Appointment

admin.site.register(Service)
admin.site.register(Master)
admin.site.register(Appointment)