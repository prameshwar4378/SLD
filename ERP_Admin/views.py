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
    drivers=Driver.objects.select_related()
    form=DriverRegistrationForm()
    return render(request, "admin_drivers_list.html",{'form':form,'drivers':drivers})


def create_driver(request):
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
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
    technicians=Technician.objects.select_related()
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
 