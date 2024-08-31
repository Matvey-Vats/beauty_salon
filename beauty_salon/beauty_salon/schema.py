import graphene
from graphene_django.types import DjangoObjectType
from services.models import Appointment, Service
from users.models import User

# Определение типов для моделей Django
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment
        fields = ("id", "service", "master", "client", "date", "status")

class ServiceType(DjangoObjectType):
    class Meta:
        model = Service
        fields = ("id", "name", "description", "price", "duration", "masters")

# Определение запросов
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_appointments = graphene.List(AppointmentType)
    all_services = graphene.List(ServiceType)

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_appointments(root, info):
        return Appointment.objects.all()

    def resolve_all_services(root, info):
        return Service.objects.all()

# Определение мутаций
class CreateAppointment(graphene.Mutation):
    class Arguments:
        service_id = graphene.ID(required=True)
        master_id = graphene.ID(required=True)
        client_id = graphene.ID(required=True)
        date = graphene.DateTime(required=True)
    
    appointment = graphene.Field(AppointmentType)

    @classmethod
    def mutate(cls, root, info, service_id, master_id, client_id, date):
        appointment = Appointment(
            service_id=service_id,
            master_id=master_id,
            client_id=client_id,
            date=date
        )
        appointment.save()
        return CreateAppointment(appointment=appointment)

class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointment.Field()

# Объединение запросов и мутаций в схему
schema = graphene.Schema(query=Query, mutation=Mutation)
