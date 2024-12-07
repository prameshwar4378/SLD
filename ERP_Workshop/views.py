from django.shortcuts import render,redirect
from .forms import *
from django.http import JsonResponse
from ERP_Admin.models import Product,Model
import openpyxl
from django.contrib import messages


def dashboard(request):
    return render(request, "workshop_dashboard.html")

def breakdown_alerts(request):
    return render(request, "workshop_breakdown_alerts.html")

def job_card_management(request):
    return render(request, "workshop_job_card_management.html")

def maintenance_logs(request):
    return render(request, "workshop_maintenance_logs.html")

def maintenance_schedule(request):
    return render(request, "workshop_maintenance_schedule.html")


def product_list(request):
    form= ProductForm()
    product=Product.objects.all().order_by('-id')
    return render(request, "workshop_product_list.html",{'form':form,'product':product})

def import_products(request):
    if request.method == "POST":
        excel_file = request.FILES.get('product_file')
        if excel_file:
            try:
                # Load the Excel workbook
                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                
                data_to_insert = []
                model_cache = {}  # Cache to avoid repeated DB queries
                
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    product_code = row[0]
                    product_name = row[1]
                    model_name = row[2]  # Assuming the model name is provided in the Excel file
                    description = row[3] or ""
                    sale_price = row[4] or 0.0
                    minimum_stock_alert = row[5] or 0
                    available_stock = row[6] or 0

                    # Check if the product_code already exists
                    if Product.objects.filter(product_code=product_code).exists():
                        messages.error(request, f"Product with code {product_code} already exists")
                        continue

                    # Retrieve or create the model instance
                    if model_name not in model_cache:
                        model_instance, created = Model.objects.get_or_create(model_name=model_name)
                        model_cache[model_name] = model_instance
                    else:
                        model_instance = model_cache[model_name]

                    # Add the product data to the batch insert list
                    data_to_insert.append(
                        Product(
                            product_code=product_code,
                            product_name=product_name,
                            model=model_instance,
                            description=description,
                            sale_price=sale_price,
                            minimum_stock_alert=minimum_stock_alert,
                            available_stock=available_stock,
                        )
                    )

                # Bulk insert all the valid products
                Product.objects.bulk_create(data_to_insert)
                messages.success(request, 'Products imported successfully.')

            except Exception as e:
                messages.error(request, f"Error occurred during import: {str(e)}")
        else:
            messages.error(request, 'No file selected.')

        return redirect('/admin/product-list')
    return redirect('/admin/product-list')


def purchase_list(request):
    form= PurchaseForm()
    purchase=Purchase.objects.all().order_by('-id')
    return render(request, "workshop_purchase_list.html",{'form':form,'purchase':purchase})

def create_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True, 'message': 'Purchase created successfully!'})
            except ValidationError as e:
                # Handle explicit model-level validation errors
                return JsonResponse({'success': False, 'errors': {'non_field_errors': str(e)}}, status=400)
        else:
            # Handle form errors, including unique constraint violations
            errors = {
                field: [str(error) for error in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def reports(request):
    return render(request, "workshop_reports.html")
