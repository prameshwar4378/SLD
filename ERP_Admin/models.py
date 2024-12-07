from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_account = models.BooleanField(default=False)
    is_workshop = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Custom reverse relation name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Custom reverse relation name
        blank=True
    )

    def __str__(self):
        return self.username
 

class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return f"{self.vehicle_name} ({self.vehicle_number})"
    
class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    driver_name = models.CharField(max_length=20, null=False, blank=False)
    license_number = models.CharField(max_length=20, unique=True, null=False, blank=False)
    adhaar_number = models.CharField(max_length=20, unique=True, null=True, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=False)
    def __str__(self):
        return f"{self.driver_name} - {self.user.username}"
    
class Technician(models.Model):
    technician_name = models.CharField(max_length=100, verbose_name="Technician Name")
    adhaar_number = models.CharField(max_length=20, unique=True, verbose_name="Aadhaar Number")
    mobile_number = models.CharField(max_length=10, unique=True, verbose_name="Mobile Number")
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True, verbose_name="Email Address")
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    date_joined = models.DateField(auto_now_add=True, verbose_name="Date Joined")

    def __str__(self):
        return f"{self.technician_name}"

    class Meta:
        verbose_name = "Technician"
        verbose_name_plural = "Technicians"