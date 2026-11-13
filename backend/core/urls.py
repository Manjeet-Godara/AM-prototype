from django.urls import path, include
from . import views

urlpatterns = [
    path('agents/register/', views.register_agent, name='agents_register'),
    path('tests/register/', views.register_test, name='tests_register'),
    path('events/receive/', views.receive_event, name='receive_event'),
]