from django.urls import path
from coach import views

urlpatterns = [
    path('home', views.coach_home, name='coach_home'),
    path('clients', views.coach_clients, name='coach_clients'),
    path('documents', views.coach_documents, name='coach_documents'),
    path('dashboard', views.coach_dashboard, name='coach_dashboard'),
    path('smessages', views.coach_messages, name='coach_messages'),
]
