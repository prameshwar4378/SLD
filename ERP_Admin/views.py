from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
import openpyxl
from .forms import *
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login as authlogin, authenticate,logout as DeleteSession

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages


from django.core.cache import cache

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.core.cache import cache
from .models import *

@receiver(post_save, sender=Product)
def update_cache_on_save(sender, instance, **kwargs):
    products = [] 
    for product in Product.objects.select_related('model').all().order_by('-id'):
        product_data = model_to_dict(product)
        product_data['model'] = {
            'model_name': product.model.model_name,   
        }
        products.append(product_data)
    cache.set('cache_products', products, timeout=None)

@receiver(post_delete, sender=Product)
def update_cache_on_delete(sender, instance, **kwargs):
    update_cache_on_save(sender, instance)  #  




@receiver(post_save, sender=Driver)
def update_driver_cache_on_save(sender, instance, **kwargs):
    # Use select_related to fetch the related CustomUser data in one query
    drivers = Driver.objects.select_related('user').all().values(
        'id', 'driver_name', 'license_number', 'phone_number', 'adhaar_number', 'address', 'date_of_birth', 'date_joined',
        'user__username', 'user__email', 'user__first_name', 'user__last_name'  # Add related fields from CustomUser
    )
    # Update the cache with the latest driver data, including CustomUser related fields
    cache.set('cache_drivers', list(drivers), timeout=None)
    print("Driver cache updated on save")

@receiver(post_delete, sender=Driver)
def update_driver_cache_on_delete(sender, instance, **kwargs):
    # Use select_related to fetch related CustomUser data after a delete
    drivers = Driver.objects.select_related('user').all().values(
        'id', 'driver_name', 'license_number', 'phone_number', 'adhaar_number', 'address', 'date_of_birth', 'date_joined',
        'user__username', 'user__email', 'user__first_name', 'user__last_name'   
    )
    # Update the cache to reflect the deletion
    cache.set('cache_drivers', list(drivers), timeout=None)
    print("Driver cache updated on delete")



    
 
@receiver(post_save, sender=Technician)
def update_technician_cache_on_save(sender, instance, **kwargs):
    # Retrieve all technicians data and serialize it if needed
    technicians = Technician.objects.all().values(
        'id', 'technician_name', 'adhaar_number', 'mobile_number', 'email', 'address', 'date_of_birth', 'date_joined'
    )
    # Update cache with the latest technicians data
    cache.set('cache_technicians', list(technicians), timeout=None)
    print("Technician cache updated on save")

@receiver(post_delete, sender=Technician)
def update_technician_cache_on_delete(sender, instance, **kwargs):
    # Retrieve all technicians data after delete
    technicians = Technician.objects.all().values(
        'id', 'technician_name', 'adhaar_number', 'mobile_number', 'email', 'address', 'date_of_birth', 'date_joined'
    )
    # Update the cache to reflect the deletion
    cache.set('cache_technicians', list(technicians), timeout=None)
    print("Technician cache updated on delete")





def login(request): 
    if request.user.is_authenticated:
        return redirect_user_based_on_role(request, request.user)
    
    if request.method == 'POST': 
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect_user_based_on_role(request, user)
        else:
            messages.error(request, 'Oops...! User does not exist. Please try again.')
    
    return render(request, 'login.html')

def redirect_user_based_on_role(request, user):
    """Helper function to redirect users based on their role."""
    if user.is_superuser:
        return redirect('/developer/dashboard')
    elif user.is_admin:
        return redirect('/admin/dashboard')
    elif user.is_workshop:
        return redirect('/workshop/dashboard')
    elif user.is_account:
        return redirect('/account/dashboard')
    else:
        messages.error(request, 'Unauthorized user role.')
        return redirect('login')

def logout(request):
    DeleteSession(request)
    return redirect('/login')

def dashboard(request):
    return render(request, "admin_dashboard.html")

def notifications(request):
    return render(request, "admin_notifications.html")

def financial_management(request):
    return render(request, "admin_financial_management.html")

def live_status(request):
    return render(request, "admin_live_status.html")

def maintenance(request):
    return render(request, "admin_maintenance.html")

def report(request):
    return render(request, "admin_report.html")

def user_management(request):
    form=UserRegistraionForm()
    users=CustomUser.objects.filter(Q(is_admin=True) | Q(is_workshop=True) | Q(is_account=True))
    return render(request, "admin_user_management.html",{'form':form,'users':users})

def create_user(request):
    if request.method == 'POST':
        form = UserRegistraionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True, 'message': 'User created successfully!'})
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




def drivers_list(request):
    drivers = cache.get('cache_drivers')
    if not drivers:
    # If data is not in the cache, retrieve from the database and set the cache
        drivers = Driver.objects.select_related('user').all().values(
            'id', 'driver_name', 'license_number', 'phone_number', 'adhaar_number', 'address', 'date_of_birth', 'date_joined',
            'user__username', 'user__email', 'user__first_name', 'user__last_name'
        )
        cache.set('cache_drivers', list(drivers), timeout=None)
    form=DriverRegistrationForm()
    return render(request, "admin_drivers_list.html",{'form':form,'drivers':drivers})


def create_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                print("Form data is valid")
                print(form.cleaned_data)
                form.save()
                return JsonResponse({'success': True, 'message': 'Driver created successfully!'})
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

def delete_driver(request, id):
    driver = get_object_or_404(Driver, id=id)
    if driver:
        driver.delete()
        messages.success(request, 'Driver deleted successfully.')
    return redirect('/admin/drivers-list')


# vehical data start
def vehicle_list(request):
    vehicle = Vehicle.objects.select_related()
    form = VehicleForm()  # Pass the form for vehicle creation
    return render(request, "admin_vehicle_list.html", {'vehicle': vehicle, 'form': form})

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            try:
                fm=form.save()
                messages.success(request,"Vehiccle created successfully!")
                return JsonResponse({'success': True, 'message': 'Vehiccle created successfully!'})
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
 

def import_vehicles(request):
    if request.method == "POST":
        excel_file = request.FILES.get('vehicle_file')
        if excel_file:
            try:
                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                data_to_insert = []
                for row in worksheet.iter_rows(min_row=2, values_only=True):
                    vehicle_number = row[0]
                    vehicle_name = row[1]

                    if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
                        messages.error(request, f"Vehicle with number {vehicle_number} already exists")
                        return redirect('/admin/vehicle-list')
                    
                    if vehicle_number and vehicle_name:
                        data_to_insert.append(Vehicle(vehicle_number=vehicle_number,vehicle_name=vehicle_name))
                
                Vehicle.objects.bulk_create(data_to_insert)
                messages.success(request, 'Data Imported and Updated Successfully')
            except Exception as e:
                messages.error(request, f'Error occurred during import: {str(e)}')
        else:
            messages.error(request, 'No file selected.')
        
        return redirect('/admin/vehicle-list')
    return redirect('/admin/vehicle-list')

def delete_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    if vehicle:
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully.')
    return redirect('/admin/vehicle-list')



def technician_list(request):
    technicians=cache.get('cache_technicians')
    if not technicians:
        technicians = Technician.objects.all().values(
            'id', 'technician_name', 'adhaar_number', 'mobile_number', 'email', 'address', 'date_of_birth', 'date_joined'
        )
        cache.set('cache_technicians', list(technicians), timeout=None)
    form = TechnicianRegistrationForm()
    return render(request, "admin_technician_list.html",{'form':form,'technicians':technicians})

def create_technician(request):
    if request.method == 'POST':
        form = TechnicianRegistrationForm(request.POST)
        if form.is_valid():
            try:
                fm=form.save()
                messages.success(request,"Technician created successfully!")
                return JsonResponse({'success': True, 'message': 'Technician created successfully!'})
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
 
def delete_technician(request, id):
    technician = get_object_or_404(Technician, id=id)
    if technician:
        technician.delete()
        messages.success(request, 'Technician deleted successfully.')
    return redirect('/admin/technician-list')








from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
 
# Create a view to handle login and return token
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response
 