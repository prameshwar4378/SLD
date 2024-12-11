from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.http import JsonResponse
from ERP_Admin.models import Product,Model,Purchase
import openpyxl
from django.contrib import messages
from django.core.cache import cache
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
    form = ProductForm()
    products = cache.get('cache_products')
    if not products: 
        products = list(Product.objects.all().order_by('-id').values())
        cache.set('cache_products', products, timeout=None)
    return render(request, "workshop_product_list.html", {'form': form, 'product': products})


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True, 'message': 'Product created successfully!'})
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
                        return redirect('/workshop/product-list')
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

        return redirect('/workshop/product-list')
    return redirect('/workshop/product-list')

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if product:
        product.delete()
        messages.success(request, 'Product deleted successfully.')
    return redirect('/workshop/product-list')


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
                messages.success(request,"Purchase created successfully!")
                return redirect('/workshop/purchase-list/')
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

def get_product_details(request):
    product_code = request.GET.get('product_code')  # Get the product code from the request
    if product_code:
        try:
            product = get_object_or_404(Product, product_code=product_code)  
            data = {        
                'id': product.id,
                'product_name': product.product_name,
                'product_rate': product.sale_price,  # Ensure this field exists in your model
                'product_code': product.product_code,           # Include any other necessary fields
            }
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid Product Code'}, status=400)


def delete_purchase(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    if purchase:
        purchase.delete()
        messages.success(request, 'Bill deleted successfully.')
    return redirect('/workshop/purchase-list')

def purchase_item_list(request,id):
    purchase=get_object_or_404(Purchase, id=id)
    item=PurchaseItem.objects.all().order_by('-id')
    product_data = list(Product.objects.select_related('model'))
    cache.set('product_data', product_data, timeout=300)  # Store for 300 seconds
    product_data = cache.get('product_data')
    if request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        product_id=request.POST.get('product_id') 
        if form.is_valid(): 
            fm=form.save(commit=False)
            fm.purchase=Purchase.objects.get(id=id)
            fm.product=Product.objects.get(id=product_id)
            fm.save()
        else:
            print("Form errors:", form.errors)
    form = PurchaseItemForm()
    return render(request, "workshop_purchase_item_list.html",{'form':form,'item':item,'purchase':purchase,'product_data':product_data})

# def create_purchase_item(request):

#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         purchase_id = request.POST.get('purchase_id')
#         product_code = request.POST.get('product_code')
#         product_name = request.POST.get('product_name')
#         quantity = request.POST.get('quantity')
#         rate = request.POST.get('rate')
#         total_amount = request.POST.get('total_amount')
 
#         if not (product_code and product_name and quantity and rate and total_amount):
#             return JsonResponse({'error': 'All fields are required.'}, status=400)

#         try:
#             # Fetch the product
#             print("Enter in login")
#             product = Product.objects.get(id=product_id)
#             purchase = Purchase.objects.get(id=purchase_id)
#             # Save the purchase item
#             purchase_item = PurchaseItem.objects.create(
#                 product=product,
#                 purchase=purchase,
#                 quantity=int(quantity),
#                 cost_per_unit=float(rate),
#                 total_amount=float(total_amount)
#             )

#             return JsonResponse({'message': 'Purchase item successfully created.'}, status=201)
#         except Product.DoesNotExist:
#             return JsonResponse({'error': 'Product not found.'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)


def delete_purchase_item(request, id):
    item = get_object_or_404(PurchaseItem, id=id)
    purchase_id=item.purchase.id
    if item:
        item.delete()
        messages.success(request, 'Item deleted successfully.')
    return redirect(f'/workshop/purchase-item-list/{purchase_id}')


def reports(request):
    return render(request, "workshop_reports.html")
