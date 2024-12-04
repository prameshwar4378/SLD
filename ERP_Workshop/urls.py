from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='workshop_dashboard'),
    path('breakdown-alerts/', views.breakdown_alerts, name='workshop_breakdown_alerts'),
    path('job-card-management/', views.job_card_management, name='workshop_job_card_management'),
    path('maintenance-logs/', views.maintenance_logs, name='workshop_maintenance_logs'),
    path('maintenance-schedule/', views.maintenance_schedule, name='workshop_maintenance_schedule'),
    path('reports/', views.reports, name='workshop_reports'),
]

