# nonconformity/forms.py

from django import forms
from .models import NonConformity

class NonConformityForm(forms.ModelForm):
    class Meta:
        model = NonConformity
        fields = ['app', 'description', 'photo']
        widgets = {
            'app': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
