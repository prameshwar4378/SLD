# forms.py

from django import forms
from .models import Vehicle

from django.contrib.auth.forms import UserCreationForm
from .models import *

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re

        
class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
 
 
class UserRegistraionForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name','last_name', 'password1', 'password2','is_admin','is_account','is_workshop']
 

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_name']  # Fields to include in the form

    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data.get('vehicle_number') 
        if Vehicle.objects.filter(vehicle_number=vehicle_number).exists():
            raise ValidationError("This Vehicle number is already registered.")
        return vehicle_number


class DriverRegistrationForm(UserCreationForm):
    driver_name = forms.CharField(max_length=20, required=True, label="Driver Name")
    adhaar_number = forms.CharField(max_length=20, required=True, label="Aadhaar Number", widget=forms.TextInput(attrs={'oninput': 'generate_username()',}))
    license_number = forms.CharField(max_length=20, required=True, label="License Number")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    adhaar_card_photo=forms.FileField(required=False, label="Upload Adhaar Card")
    driving_license_photo=forms.FileField(required=False, label="Upload Driving License")
    profile_photo=forms.FileField(required=False, label="Upload Profile Photo")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Address")
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Date of Birth"
    )
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Date Joined"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
        widgets={ 
            'username': forms.TextInput(attrs={'readonly': True }), 
        }

    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number')
        if not re.match(r"^[A-Z0-9-]+$", license_number):
            raise ValidationError("License number can only contain letters, numbers, and hyphens.")
        if Driver.objects.filter(license_number=license_number).exists():
            raise ValidationError("This license number is already registered.")
        return license_number

    def clean_adhaar_number(self):
        adhaar_number = self.cleaned_data.get('adhaar_number')
        if not re.match(r"^\d{12}$", adhaar_number):  # Aadhaar must be 12 digits
            raise ValidationError("Aadhaar number must be a 12-digit number.")
        if Driver.objects.filter(adhaar_number=adhaar_number).exists():
            raise ValidationError("This Aadhaar number is already registered.")
        return adhaar_number

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r"^\d{10}$", phone_number):  # Validate exactly 10 digits
            raise ValidationError("Phone number must be 10 digits.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            fm=user
            fm.is_driver=True
            fm.save()
            # Create Driver instance
            Driver.objects.create(
                user=user, 
                driver_name=self.cleaned_data['driver_name'],
                adhaar_number=self.cleaned_data['adhaar_number'],
                license_number=self.cleaned_data['license_number'],
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data.get('address'),
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                date_joined=self.cleaned_data.get('date_joined'),
                adhaar_card_photo=self.cleaned_data.get('adhaar_card_photo'),
                driving_license_photo=self.cleaned_data.get('driving_license_photo'),
                profile_photo=self.cleaned_data.get('profile_photo')
            )
        return user
    



class TechnicianRegistrationForm(forms.ModelForm):
    
    adhaar_card=forms.FileField(required=False, label="Upload Adhaar Card")
    profile_photo=forms.FileField(required=False, label="Upload Profile Photo")
    additional_docs=forms.FileField(required=False, label="Upload Additional Document")

    technician_name = forms.CharField(
        max_length=100, 
        required=True, 
        label="Technician Name",
            )
    adhaar_number = forms.CharField(
        max_length=12, 
        required=True, 
        label="Aadhaar Number", 
            )
    mobile_number = forms.CharField(
        max_length=10, 
        required=True, 
        label="Mobile Number", 
            )
    email = forms.EmailField(
        required=False, 
        label="Email Address", 
            )
    address = forms.CharField(
        required=False, 
        label="Address", 
            )
    date_of_birth = forms.DateField(
        required=False, 
        label="Date of Birth", 
            )

    class Meta:
        model = Technician
        fields = [
            'technician_name',
            'adhaar_number',
            'mobile_number',
            'email',
            'address',
            'date_of_birth',
        ]

    def clean_adhaar_number(self):
        adhaar_number = self.cleaned_data.get('adhaar_number')
        if not re.match(r"^\d{12}$", adhaar_number):  # Aadhaar must be 12 digits
            raise ValidationError("Aadhaar number must be a 12-digit number.")
        if Technician.objects.filter(adhaar_number=adhaar_number).exists():
            raise ValidationError("This Aadhaar number is already registered.")
        return adhaar_number

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not re.match(r"^\d{10}$", mobile_number):  # Validate exactly 10 digits
            raise ValidationError("Mobile number must be 10 digits.")
        if Technician.objects.filter(mobile_number=mobile_number).exists():
            raise ValidationError("This mobile number is already registered.")
        return mobile_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Technician.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        technician = super().save(commit=False)
        if commit:
            technician.save()
        return technician
    