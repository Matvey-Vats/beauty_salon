from django.urls import path


from . import views

urlpatterns = [
    path('notifications/', views.MessagesListView.as_view()),
]
