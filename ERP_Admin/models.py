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
    mobile_number = models.CharField(max_length=15, null=False, blank=False)
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=False)
    adhaar_card_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    pan_card_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    driving_license_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    profile_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    def __str__(self):
        return f"{self.driver_name} - {self.user.username}"
    
class Technician(models.Model):
    technician_name = models.CharField(max_length=100, verbose_name="Technician Name")
    adhaar_number = models.CharField(max_length=20, unique=True, verbose_name="Aadhaar Number")
    mobile_number = models.CharField(max_length=10, unique=True, verbose_name="Mobile Number")
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True, verbose_name="Email Address")
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    date_joined = models.DateField(auto_now_add=True, verbose_name="Date Joined") 
    pan_card=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    adhaar_card=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    profile_photo=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    additional_docs=models.FileField(upload_to="Documents", max_length=None, null=True, blank=True)
    def __str__(self):
        return f"{self.technician_name}"

    class Meta:
        verbose_name = "Technician"
        verbose_name_plural = "Technicians"


class Party(models.Model):
    business_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    document1=models.FileField(upload_to="ClientDocuments", max_length=None, null=True, blank=True)
    document2=models.FileField(upload_to="ClientDocuments", max_length=None, null=True, blank=True)
    document3=models.FileField(upload_to="ClientDocuments", max_length=None, null=True, blank=True)

    def __str__(self):
        return self.business_name
    

 
class Model(models.Model):
    model_name = models.CharField(max_length=50, unique=True, db_index=True) 
    def __str__(self):
        return self.model_name


class Product(models.Model):
    product_code = models.CharField(max_length=20, unique=True, db_index=True)
    product_name = models.CharField(max_length=100, db_index=True)
    model = models.ForeignKey(Model, related_name='items', null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Use DecimalField for monetary values
    minimum_stock_alert = models.PositiveIntegerField(default=0)
    available_stock = models.PositiveIntegerField(default=0, db_index=True, null=True, blank=True)
    product_image=models.ImageField(upload_to="Product Images", height_field=None, width_field=None, max_length=500, null=True, blank=True)
    def __str__(self):
        return self.product_name

PURCHASE_GST=(
    ('GST BILL','GST BILL'),
    ('Without GST BILL','Without GST BILL')
)
class Purchase(models.Model):
    bill_no = models.CharField(max_length=50, db_index=True, unique=True, null=False, blank=False)
    supplier_name = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    bill_type = models.CharField(max_length=30, db_index=True, choices=PURCHASE_GST)
    bill_date = models.DateField(auto_now_add=False, db_index=True)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    bill_file = models.FileField(upload_to="Purchase Bill", null=True, blank=True)
    def __str__(self):
        return f"Purchase #{self.bill_no} on {self.bill_date}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Update product stock on save
        if self.pk is None:  # Only add stock if it's a new record
            self.product.available_stock += self.quantity
        else:  # If updated, adjust stock accordingly
            original = PurchaseItem.objects.get(pk=self.pk)
            self.product.available_stock += self.quantity - original.quantity
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Adjust stock on deletion
        self.product.available_stock -= self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in Purchase #{self.purchase.id}"


from django.db import models
from django.core.validators import MinValueValidator

JOB_CARD_STATUS = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]


class JobCard(models.Model):
    job_card_number = models.CharField(max_length=20, unique=True, editable=False)
    technician = models.ForeignKey('Technician', related_name='job_cards',  on_delete=models.CASCADE, null=True, blank=True)
    driver= models.ForeignKey('Driver', related_name='job_cards',  on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    reported_defect = models.TextField()
    completed_action = models.TextField(null=True, blank=True)
    party = models.ForeignKey('Party', related_name='job_cards', on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey('Vehicle', related_name='job_cards', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=JOB_CARD_STATUS, default='pending')
    labour_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        if not self.id:
            last_job_card = JobCard.objects.order_by('-id').first()
            if last_job_card:
                last_number = int(last_job_card.job_card_number.split('-')[1])
                self.job_card_number = f"JOB-{last_number + 1}"
            else:
                self.job_card_number = "JOB-1"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Job Card {self.job_card_number} for Vehicle ID {self.vehicle.id}"


class JobCardItem(models.Model):
    job_card = models.ForeignKey(JobCard, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='job_card_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    def __str__(self):
        return f"Item {self.product.id} for Job Card {self.job_card.job_card_number}"

 

