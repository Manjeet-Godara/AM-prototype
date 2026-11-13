from django.urls import path, include
from . import views

urlpatterns = [
    path('agents/register/', views.register_agent, name='agents_register'),
    path('tests/register/', views.register_test, name='tests_register'),
    path('events/receive/', views.receive_event, name='receive_event'),
    path('systems/', views.get_systems, name='get_systems'),
    path('systems/<int:system_id>/tests/', views.get_system_tests, name='get_system_tests'),
    path('tests/<int:test_id>/runs/', views.get_test_runs, name='get_test_runs'),
    path('runs/<int:run_id>/', views.get_run_details, name='get_run_details'),
]