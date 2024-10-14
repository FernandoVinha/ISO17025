from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, RelationshipType, Companies, Contacts, Invitation

# ====== Custom User Forms ======

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'role')
    
    # Custom validation to ensure first_name and last_name are not empty
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("First name is required.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        return last_name

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'role')

# ====== RelationshipType Form ======

class RelationshipTypeForm(forms.ModelForm):
    class Meta:
        model = RelationshipType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Relationship Type'}),
        }

# ====== Companies Form ======

class CompaniesForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ['name', 'email', 'phone', 'profile_image', 'relationship_type']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Company Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Company Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Company Phone'}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  # Widget for file input
            'relationship_type': forms.Select(),
        }

# ====== Contacts Form ======

class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['name', 'email', 'phone', 'profile_image', 'position', 'company']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Contact Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Contact Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter Contact Phone'}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  # Widget for file input
            'position': forms.TextInput(attrs={'placeholder': 'Enter Position'}),
            'company': forms.Select(),
        }

# ====== Invitation Form ======

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email for invitation'}),
        }
