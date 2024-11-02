# forms.py
from django import forms
from .models import Methodology, MethodologySupply

class MethodologyForm(forms.ModelForm):
    class Meta:
        model = Methodology
        fields = ['title', 'description', 'author', 'equipment']

class MethodologySupplyForm(forms.ModelForm):
    class Meta:
        model = MethodologySupply
        fields = ['supply', 'quantity', 'unit']
