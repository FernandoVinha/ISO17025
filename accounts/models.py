# ISO17025/accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.crypto import get_random_string
from simple_history.models import HistoricalRecords

class RelationshipType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("view_relationshiptype", "Can view Relationship Type"),
            ("create_relationshiptype", "Can create Relationship Type"),
            ("edit_relationshiptype", "Can edit Relationship Type"),
            ("delete_relationshiptype", "Can delete Relationship Type"),
        ]

    def __str__(self):
        return self.name

class Companies(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.SET_NULL, null=True, related_name='companies')
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("view_companies", "Can view Companies"),
            ("create_companies", "Can create Companies"),
            ("edit_companies", "Can edit Companies"),
            ("delete_companies", "Can delete Companies"),
        ]

    def __str__(self):
        return f"{self.name} - {self.relationship_type.name if self.relationship_type else 'No Type'}"

class Contacts(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=100, help_text="Position or job title")
    company = models.ForeignKey(Companies, on_delete=models.CASCADE, related_name='company_contacts')
    history = HistoricalRecords()

    class Meta:
        permissions = [
            ("view_contacts", "Can view Contacts"),
            ("create_contacts", "Can create Contacts"),
            ("edit_contacts", "Can edit Contacts"),
            ("delete_contacts", "Can delete Contacts"),
        ]

    def __str__(self):
        return f"{self.name} - {self.position} at {self.company.name}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The user must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('supplier', 'Supplier'),
        ('maintenance', 'Maintenance'),
        ('employee', 'Employee'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    profile_image = models.ImageField(upload_to='user_profiles/', blank=True, null=True, help_text="User profile image")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        permissions = [
            ("can_generate_invite", "Can generate invitation link"),  # Permissão específica para o app de usuários
        ]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

class Invitation(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=32, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=32)
            # Garante que o token seja único
            while Invitation.objects.filter(token=self.token).exists():
                self.token = get_random_string(length=32)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invitation for {self.email}"
