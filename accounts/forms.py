from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, RelationshipType, Invitation

# ====== Custom User Forms ======

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
    
    # Validação customizada para garantir que o primeiro e o último nome estejam preenchidos
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
        error_messages = {
            'email': {
                'unique': "This email is already in use.",
            },
        }

# ====== RelationshipType Form ======

class RelationshipTypeForm(forms.ModelForm):
    class Meta:
        model = RelationshipType
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Relationship Type'}),
        }


# ====== Invitation Form ======

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email for invitation'}),
        }
        error_messages = {
            'email': {
                'unique': "An invitation for this email already exists.",
                'invalid': "Enter a valid email address.",
            },
        }

# ====== Profile Update Form ======

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
        error_messages = {
            'first_name': {
                'required': "First name is required.",
            },
            'last_name': {
                'required': "Last name is required.",
            },
        }

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and image.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("Image file too large ( > 5MB ).")
        return image
