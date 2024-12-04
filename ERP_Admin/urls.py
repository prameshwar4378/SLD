from django.urls import path
from . import views

urlpatterns = [
    # path('login-token', CustomAuthToken.as_view(), name='api_token_auth'),
    path('dashboard/', views.dashboard, name='admin_dashboard'),
    path('notifications/', views.notifications, name='admin_notifications'),
    path('financial-management/', views.financial_management, name='admin_financial_management'),
    path('live-status/', views.live_status, name='admin_live_status'),
    path('maintenance/', views.maintenance, name='admin_maintenance'),
    path('report/', views.report, name='admin_report'),
    path('user-management/', views.user_management, name='admin_user_management'),
    path('drivers-list/', views.drivers_list, name='admin_drivers_list'),
    path('vehicle-list/', views.vehicle_list, name='admin_vehicle_list'),
    path('create_vehicle/', views.create_vehicle, name='admin_create_vehicle'),
    path('import_vehicles/', views.import_vehicles, name='admin_import_vehicles'),
    path('delete_vehicle/<int:id>/', views.delete_vehicle, name='admin_delete_vehicle'),
    path('technician-list/', views.technician_list, name='admin_technician_list'),

]