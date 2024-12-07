from django import forms
from django.core.exceptions import ValidationError
from ERP_Admin.models import Purchase, PurchaseItem

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