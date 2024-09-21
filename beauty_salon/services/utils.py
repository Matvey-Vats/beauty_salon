from django_filters import rest_framework as filters
from .models import Service, Appointment, Master
from datetime import timedelta
from django.utils import timezone

from django.utils import timezone

def get_master_schedule(master, date=None):
    if date is None:
        date = timezone.now().date()

    appointments = Appointment.objects.filter(
        master=master,
        date__date=date
    ).order_by('date')
    
    schedule = {}
    for appointment in appointments:

        start_time = appointment.date.strftime('%Y-%m-%d %H:%M')
        end_time = (appointment.date + appointment.service.duration).strftime('%Y-%m-%d %H:%M')
        
        schedule[start_time] = {
            'service': appointment.service.name,
            'client': appointment.client.username,
            'start_time': start_time,
            'end_time': end_time
        }
    
    return schedule




# def get_master_schedule(master, start_date, end_date):
    
#     appointments = Appointment.objects.filter(
#         master=master,
#         date__gte=start_date,
#         date__lte=end_date,
#         status="scheduled",
#     ).order_by("date")

#     schedule = []
    
#     workday_start = start_date.replace(hour=9, minute=0)
#     workday_end = end_date.replace(hour=18, minute=0)
    
#     current_time = timezone.now()
    
#     for appointment in appointments:
#         if appointment.date > current_time:
#             free_period = (current_time, appointment.date)
#             schedule.append({'status': 'free', 'start': free_period[0], 'end': free_period[1]})
        
#         appointment_end = appointment.date + timedelta(minutes=appointment.service.duration)
#         schedule.append({'status': 'busy', 'start': appointment.date, 'end': appointment_end})
        
#         current_time = appointment_end
        
#     if current_time < workday_end:
#         schedule.append({'status': 'free', 'start': current_time, 'end': workday_end})
    
#     return schedule


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class ServiceFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name='name')
    price = filters.RangeFilter()
    
    
class AppointmentFilter(filters.FilterSet):
    status = filters.ChoiceFilter(
        choices=Appointment.STATUS_CHOICES,
        label="Status",
        empty_label="All"
    )
    
    date = filters.DateFilter(field_name='date', lookup_expr='exact', label='Date')
    
    class Meta:
        model = Appointment
        fields = ('status', 'date')