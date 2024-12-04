from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_account = models.BooleanField(default=False)
    is_workhouse = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.vehicle_name} ({self.vehicle_number})"
    
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    license_number = models.CharField(max_length=20, unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.license_number}"