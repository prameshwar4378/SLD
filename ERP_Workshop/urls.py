from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='workshop_dashboard'),
    path('breakdown-alerts/', views.breakdown_alerts, name='workshop_breakdown_alerts'),
    path('job-card-management/', views.job_card_management, name='workshop_job_card_management'),
    path('maintenance-logs/', views.maintenance_logs, name='workshop_maintenance_logs'),
    path('maintenance-schedule/', views.maintenance_schedule, name='workshop_maintenance_schedule'),

    path('product-list/', views.product_list, name='workshop_product_list'),
    path('create-product/', views.create_product, name='workshop_create_product'),
    path('import-product/', views.import_products, name='workshop_import_products'),
    path('delete-product/<int:id>', views.delete_product, name='workshop_delete_product'),

    path('purchase-list/', views.purchase_list, name='workshop_purchase_list'),
    path('create-purchase/', views.create_purchase, name='workshop_create_purchase'),
    path('delete-purchase/<int:id>', views.delete_purchase, name='workshop_delete_purchase'),

    path('get_product_details/', views.get_product_details, name='workshop_get_product_details'),
    path('delete_purchase_item/<int:id>', views.delete_purchase_item, name='workshop_delete_purchase_item'),
    path('purchase-item-list/<int:id>', views.purchase_item_list, name='workshop_purchase_item_list'),

    path('reports/', views.reports, name='workshop_reports'),
]

