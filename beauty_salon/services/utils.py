from django_filters import rest_framework as filters
from .models import Service, Appointment, Master


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