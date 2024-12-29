# inventory/forms.py
from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            'name',
            'serial_number',
            'item_type',
            'supplier',
            'cost',
            'manufacturing_date',
            'expiration_date',
            'quantity',
            'unit',
            'image',
            'description',
            'responsible_user',
            'room',
        ]
        widgets = {
            'manufacturing_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
