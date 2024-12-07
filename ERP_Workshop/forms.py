from django import forms
from django.core.exceptions import ValidationError
from ERP_Admin.models import Purchase, PurchaseItem,Product

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['bill_no','bill_date', 'supplier_name', 'total_cost']
        widgets={ 
            'bill_date': forms.TextInput(attrs={'type': 'date' })
        }

    def clean_bill_no(self):
        bill_no = self.cleaned_data.get('bill_no')
        if not bill_no:
            raise ValidationError("Bill number is required.")
        if len(bill_no) < 5:
            raise ValidationError("Bill number must be at least 5 characters long.")
        # Check for uniqueness
        if Purchase.objects.filter(bill_no=bill_no).exists():
            raise ValidationError("Bill number must be unique. This number already exists.")
        return bill_no

    def clean_supplier_name(self):
        supplier_name = self.cleaned_data.get('supplier_name')
        if supplier_name and len(supplier_name) < 3:
            raise ValidationError("Supplier name must be at least 3 characters long.")
        return supplier_name

    def clean_total_cost(self):
        total_cost = self.cleaned_data.get('total_cost')
        if total_cost <= 0:
            raise ValidationError("Total cost must be greater than zero.")
        return total_cost
    



 
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_code',
            'product_name',
            'model',
            'description',
            'sale_price',
            'minimum_stock_alert',
            'available_stock',
            'product_image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'model': forms.Select(attrs={'class': 'searchable-dropdown'}),
        }

    def clean_product_code(self):
        product_code = self.cleaned_data.get('product_code')
        if not product_code:
            raise ValidationError("Product code is required.")
        if len(product_code) > 20:
            raise ValidationError("Product code cannot exceed 20 characters.")
        return product_code

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if not product_name:
            raise ValidationError("Product name is required.")
        if len(product_name) > 100:
            raise ValidationError("Product name cannot exceed 100 characters.")
        return product_name

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        if sale_price is None:
            raise ValidationError("Sale price is required.")
        if sale_price <= 0:
            raise ValidationError("Sale price must be greater than zero.")
        return sale_price

    def clean_minimum_stock_alert(self):
        minimum_stock_alert = self.cleaned_data.get('minimum_stock_alert')
        if minimum_stock_alert < 0:
            raise ValidationError("Minimum stock alert cannot be negative.")
        return minimum_stock_alert

    def clean_available_stock(self):
        available_stock = self.cleaned_data.get('available_stock')
        if available_stock < 0:
            raise ValidationError("Available stock cannot be negative.")
        return available_stock

    def clean_product_image(self):
        product_image = self.cleaned_data.get('product_image')
        if product_image:
            # Validate image size (max 500 KB)
            if product_image.size > 500 * 1024:
                raise ValidationError("Image size must not exceed 500 KB.")
            # Validate image type (optional)
            if not product_image.content_type.startswith('image/'):
                raise ValidationError("Uploaded file is not a valid image.")
        return product_image
